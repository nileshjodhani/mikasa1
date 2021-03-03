#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)


import os

from dobrot import (
    DOWNLOAD_LOCATION
)
import asyncio
import subprocess
import pyrogram
import time
from dobrot.helper_funcs.extract_link_from_message import extract_link
from dobrot.helper_funcs.download_aria_p_n import call_apropriate_function, aria_start
from dobrot.helper_funcs.download_from_link import request_download
from dobrot.helper_funcs.display_progress import progress_for_pyrogram
from dobrot.helper_funcs.youtube_dl_extractor import extract_youtube_dl_formats
from subprocess import call
from dobrot.helper_funcs.upload_to_tg import upload_to_tg
from dobrot.helper_funcs.create_compressed_archive import create_unzip
from dobrot.helper_funcs.newc import convert_file, convert_link

async def incoming_message_f(client, message):
    """/leech command"""
    i_m_sefg = await message.reply_text("processing", quote=True)
    is_zip = False
    is_unzip = False
    is_convert = False
    if len(message.command) > 1:
        if message.command[1] == "archive":
            is_zip = True
        elif message.command[1] == "unzip":
            is_unzip = True
        elif message.command[1] == "convert":
            is_convert = True
    # get link from the incoming message
    if not message.reply_to_message:
      i_m_sefg = await message.reply_text("No link or No File Found", quote=True)
    elif message.reply_to_message.document:
      hell = await message.reply_to_message.download(
        file_name = DOWNLOAD_LOCATION
        )
      sent_message_to_update_tg_p = i_m_sefg
      current_user_id = message.from_user.id
      new_download_location = os.path.join(DOWNLOAD_LOCATION,str(current_user_id),str(time.time()))
                
                
      LOGGER.info(new_download_location)         
              
      if not os.path.isdir(new_download_location):
          os.makedirs(new_download_location)
      new_download_location = new_download_location + "/"
      #i_m_sefg = await message.reply_text(text=hell, quote=True)
      with open (hell) as foe:
        for rec in foe:
          url = rec
          LOGGER.info(url)
          if "?a=view" in url:
             url = url.replace("?a=view","")
          command =[
               "youtube-dl",
               "--no-warnings",
               "--console-title",
               "-c",
               "--retries=10",
               #"--max-sleep-interval=20",
               "-o"+new_download_location+"%(title)s.%(ext)s",
               url
          ]   
          process = call(command, shell=False)
      if is_convert:
        a = os.listdir(new_download_location)
        b = a[0]
        #convert_file(new_download_location,'same',300,False)
        new_download_location = new_download_location + b
        new_download_location = os.path.abspath(new_download_location)
        convert_file(new_download_location,'same',300,False)
      to_upload_file = new_download_location
      response = {}
      LOGGER.info(response)
      user_id = sent_message_to_update_tg_p.reply_to_message.from_user.id
      final_response = await upload_to_tg(sent_message_to_update_tg_p,to_upload_file,user_id,response)
                  
                  
                  
                  
              
    else:
      sent_message_to_update_tg_p = i_m_sefg
      i_m_sefg = await message.reply_text("is not", quote=True)
      dl_url, cf_name = extract_link(message.reply_to_message)
      LOGGER.info(dl_url)
      LOGGER.info(cf_name)
      
      if dl_url is not None:
          await i_m_sefg.edit_text("extracting links")
        # start the aria2c daemon
          
          #aria_i_p = await aria_start()
          #LOGGER.info(aria_i_p)
          
          current_user_id = message.from_user.id
        # create an unique directory
          new_download_location = os.path.join(
            DOWNLOAD_LOCATION,
            str(current_user_id),
            str(time.time())
          )
          new_download_location = new_download_location + "/"
        # create download directory, if not exist
          if not os.path.isdir(new_download_location):
              os.makedirs(new_download_location)
          await i_m_sefg.edit_text("trying to download")
          url = dl_url
          command =[
               "youtube-dl",
               "--no-warnings",
               "--console-title",
               "-c",
               "--retries=10",
               #"--max-sleep-interval=20",
               "-o"+new_download_location+"%(title)s.%(ext)s",
               url
          ]
          process = call(command, shell=False)
          if is_convert:
            a = os.listdir(new_download_location)
            b = a[0]
            #convert_file(new_download_location,'same',300,False)
            new_download_location = new_download_location + b
            #convert_file(new_download_location,'same',300,False)
            conurl = convert_link(url,'same',300,False)
            i_m_sefg1 = await message.reply_text(text=conurl, quote=True)
          if is_unzip:
            a = os.listdir(new_download_location)
            b = a[0]
            new_download_location = new_download_location + b
            new_download_location = await create_unzip(new_download_location)
            to_upload_file = new_download_location
            response = {}
            LOGGER.info(response)
            user_id = current_user_id #sent_message_to_update_tg_p.reply_to_message.from_user.id
            final_response = await upload_to_tg(sent_message_to_update_tg_p,to_upload_file,user_id,response)
          else:
            to_upload_file = new_download_location
            response = {}
            LOGGER.info(response)
            user_id = current_user_id #sent_message_to_update_tg_p.reply_to_message.from_user.id
            final_response = await upload_to_tg(sent_message_to_update_tg_p,to_upload_file,user_id,response)
           
            
        # try to download the "link"
      """
          sagtus, err_message = await call_apropriate_function(
              aria_i_p,
              dl_url,
            new_download_location,
              i_m_sefg,
              is_zip,
              is_unzip
          )
          if not sagtus:
            # if FAILED, display the error message
              await i_m_sefg.edit_text(err_message)
      else:
          await i_m_sefg.edit_text("**FCUK**! wat have you entered. Please read /help")
      """

async def incoming_youtube_dl_f(client, message):
    """ /ytdl command """
    i_m_sefg = await message.reply_text("processing", quote=True)
    # LOGGER.info(message)
    # extract link from message
    dl_url, cf_name = extract_link(message.reply_to_message)
    LOGGER.info(dl_url)
    LOGGER.info(cf_name)
    if dl_url is not None:
        await i_m_sefg.edit_text("extracting links")
        current_user_id = message.from_user.id
        # create an unique directory
        user_working_dir = os.path.join(DOWNLOAD_LOCATION, str(current_user_id))
        # create download directory, if not exist
        if not os.path.isdir(user_working_dir):
            os.makedirs(user_working_dir)
        # list the formats, and display in button markup formats
        text_message, reply_markup = await extract_youtube_dl_formats(
            dl_url,
            user_working_dir
        )
        await i_m_sefg.edit_text(
            text=text_message,
            reply_markup=reply_markup
        )
    else:
        # if no links found, delete the "processing" message
        await i_m_sefg.delete()
