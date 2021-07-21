# -*- coding: utf-8 -*-

from wordcloud import WordCloud
import numpy as np

class c_wordcloud:
    def woco_pic(self, k_list, num, video_id):
        word_counts = {}
        for word in k_list:
            if len(word) > 1:
                if word not in word_counts:
                    word_counts[word] = 0
                word_counts[word] += 1
        woco = WordCloud(max_font_size=200, font_path='static/font/BMDOHYEON_ttf.ttf', background_color='white', width=800, height=800, colormap='winter').generate_from_frequencies(word_counts)
        woco.to_file('static/img/'+video_id+"_"+str(num).zfill(4)+'.png')
