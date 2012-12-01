#!/usr/bin/env python2
import unittest
import hashlib
import os
import json

from youtube_dl.FileDownloader import FileDownloader
from youtube_dl.InfoExtractors  import YoutubeIE, DailymotionIE
from youtube_dl.InfoExtractors import  MetacafeIE, BlipTVIE


class DownloadTest(unittest.TestCase):
	PARAMETERS_FILE = "test/parameters.json"
	#calculated with md5sum:
	#md5sum (GNU coreutils) 8.19

	YOUTUBE_SIZE = 1993883
	YOUTUBE_URL = "http://www.youtube.com/watch?v=BaW_jenozKc"
	YOUTUBE_FILE = "BaW_jenozKc.mp4"

	DAILYMOTION_MD5 = "d363a50e9eb4f22ce90d08d15695bb47"
	DAILYMOTION_URL = "http://www.dailymotion.com/video/x33vw9_tutoriel-de-youtubeur-dl-des-video_tech"
	DAILYMOTION_FILE = "x33vw9.mp4"

	METACAFE_SIZE = 5754305
	METACAFE_URL = "http://www.metacafe.com/watch/yt-_aUehQsCQtM/the_electric_company_short_i_pbs_kids_go/"
	METACAFE_FILE = "_aUehQsCQtM.flv"

	BLIP_MD5 = "93c24d2f4e0782af13b8a7606ea97ba7"
	BLIP_URL = "http://blip.tv/cbr/cbr-exclusive-gotham-city-imposters-bats-vs-jokerz-short-3-5796352"
	BLIP_FILE = "5779306.m4v"

	XVIDEO_MD5 = ""
	XVIDEO_URL = ""
	XVIDEO_FILE = ""


	def test_youtube(self):
		#let's download a file from youtube
		with open(DownloadTest.PARAMETERS_FILE) as f:
			fd = FileDownloader(json.load(f))
		fd.add_info_extractor(YoutubeIE())
		fd.download_single(DownloadTest.YOUTUBE_URL)
		self.assertTrue(os.path.exists(DownloadTest.YOUTUBE_FILE))
		self.assertEqual(os.path.getsize(DownloadTest.YOUTUBE_FILE), DownloadTest.YOUTUBE_SIZE)

	def test_dailymotion(self):
		with open(DownloadTest.PARAMETERS_FILE) as f:
			fd = FileDownloader(json.load(f))
		fd.add_info_extractor(DailymotionIE())
		fd.download_single(DownloadTest.DAILYMOTION_URL)
		self.assertTrue(os.path.exists(DownloadTest.DAILYMOTION_FILE))
		md5_down_file = md5_for_file(DownloadTest.DAILYMOTION_FILE)
		self.assertEqual(md5_down_file, DownloadTest.DAILYMOTION_MD5)

	def test_metacafe(self):
		#this emulate a skip,to be 2.6 compatible
		with open(DownloadTest.PARAMETERS_FILE) as f:
			fd = FileDownloader(json.load(f))
		fd.add_info_extractor(MetacafeIE())
		fd.add_info_extractor(YoutubeIE())
		fd.download_single(DownloadTest.METACAFE_URL)
		self.assertTrue(os.path.exists(DownloadTest.METACAFE_FILE))
		self.assertEqual(os.path.getsize(DownloadTest.METACAFE_FILE), DownloadTest.METACAFE_SIZE)

	def test_blip(self):
		with open(DownloadTest.PARAMETERS_FILE) as f:
			fd = FileDownloader(json.load(f))
		fd.add_info_extractor(BlipTVIE())
		fd.download_single(DownloadTest.BLIP_URL)
		self.assertTrue(os.path.exists(DownloadTest.BLIP_FILE))
		md5_down_file = md5_for_file(DownloadTest.BLIP_FILE)
		self.assertEqual(md5_down_file, DownloadTest.BLIP_MD5)

	def tearDown(self):
		if os.path.exists(DownloadTest.YOUTUBE_FILE):
			os.remove(DownloadTest.YOUTUBE_FILE)
		if os.path.exists(DownloadTest.DAILYMOTION_FILE):
			os.remove(DownloadTest.DAILYMOTION_FILE)
		if os.path.exists(DownloadTest.METACAFE_FILE):
			os.remove(DownloadTest.METACAFE_FILE)
		if os.path.exists(DownloadTest.BLIP_FILE):
			os.remove(DownloadTest.BLIP_FILE)

def md5_for_file(filename, block_size=2**20):
    with open(filename) as f:
        md5 = hashlib.md5()
        while True:
            data = f.read(block_size)
            if not data:
                break
            md5.update(data)
            return md5.hexdigest()
