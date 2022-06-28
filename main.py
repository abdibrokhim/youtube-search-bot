import logging

import requests
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler
from telegram.ext.filters import Filters
from telegram.update import Update

# YouTube search bot settings
from search import youtube_search
import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)

import settings

updater = Updater(token=settings.TELEGRAM_TOKEN)


def start(update: Update, context: CallbackContext):
    update.message \
        .reply_text('Welcome, YouTube in Telegram.\nFor Example: /search ITZY')


def search(update: Update, context: CallbackContext):
    args = context.args

    logging.info('checking args length')

    if len(args) == 0:
        update.message \
            .reply_text('For Example: /search ITZY')
    else:
        search_text = ' '.join(args)
        max_result = 5

        youtube = build(settings.YOUTUBE_API_SERVICE_NAME, settings.YOUTUBE_API_VERSION,
                        developerKey=settings.DEVELOPER_KEY)

        # Call the search.list method to retrieve results matching the specified
        # query term.
        search_response = youtube.search().list(
            q=search_text,
            part='id,snippet',
            maxResults=max_result
        ).execute()

        videos = []
        # channels = []
        # playlists = []

        # Add each result to the appropriate list, and then display the lists of
        # matching videos, channels, and playlists.
        for search_result in search_response.get('items', []):
            if search_result['id']['kind'] == 'youtube#video':
                videos.append(
                    '%s \n https://youtu.be/%s' % (search_result['snippet']['title'],
                                                   search_result['id']['videoId']))
            # elif search_result['id']['kind'] == 'youtube#channel':
            #     channels.append('%s https://youtu.be/%s' % (search_result['snippet']['title'],
            #                                  search_result['id']['channelId']))
            # elif search_result['id']['kind'] == 'youtube#playlist':
            #     playlists.append('%s https://youtu.be/%s' % (search_result['snippet']['title'],
            #                                   search_result['id']['playlistId']))

        print('Videos:\n', '\n\n'.join(videos), '\n')
        result_videos = 'Videos:\n', '\n\n'.join(videos), '\n'
        # print('Channels:\n', '\n\n'.join(channels), '\n')
        # result_channels = 'Channels:\n', '\n\n'.join(channels), '\n'
        # print('Playlists:\n', '\n\n'.join(playlists), '\n')
        # result_playlists = 'Playlists:\n', '\n\n'.join(playlists), '\n'

        logging.info('result from YouTube API')

        if len(result_videos):
            for i in result_videos:
                update.message \
                    .reply_text(i)
        else:
            update.message \
                .reply_text('no video was found')

        # if len(result_channels):
        #     for i in result_channels:
        #         update.message \
        #             .reply_text(i)
        # else:
        #     update.message \
        #         .reply_text('no channel was found')
        #
        # if len(result_playlists):
        #     for i in result_playlists:
        #         update.message \
        #             .reply_text(i)
        # else:
        #     update.message \
        #         .reply_text('no playlist was found')


dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('search', search))
dispatcher.add_handler(MessageHandler(Filters.all, start))

updater.start_polling()
updater.idle()
