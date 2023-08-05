from __future__ import print_function, division, absolute_import

import os
import queue
import time
from concurrent.futures.thread import ThreadPoolExecutor

import ddddocr
from fontTools.ttLib import TTFont
from reportlab.graphics import renderPM
from reportlab.graphics.shapes import Group, Drawing
from reportlab.graphics.shapes import Path

from ddddocr_woff.ReportLabPen import ReportLabPen


class anAlySis(object):
    def __init__(self, fontName, imagePath='images', fmt="png", clear=False):

        if clear:
            ls = os.listdir(imagePath)
            try:
                for i in ls:
                    c_path = os.path.join(imagePath, i)
                    os.remove(c_path)
                print('缓存文件已删除')
            except:
                print('没有缓存文件')
        isExists = os.path.exists(imagePath)
        if not isExists:
            print('储存图片目录未指定并且不存在，自动创建')
            os.makedirs(imagePath)

        self.fontName = fontName
        self.imagePath = imagePath
        self.fmt = fmt
        self.font = TTFont(self.fontName)
        self.gs = self.font.getGlyphSet()
        self.transmit = queue.Queue()
        self.file = queue.Queue()
        self.file_ocr = queue.Queue()
        self.file_ocr_name = queue.Queue()
        self.ocr = ddddocr.DdddOcr()
        self.glyphNames = self.font.getGlyphOrder()
        self.statistics = queue.Queue()
        self.Dict = {}

    def ttfToImage(self, transmit):

        for i in self.glyphNames:
            transmit.put(i)

    def imges_ocr(self, transmit: queue.Queue, file: queue.Queue):

        while True:
            try:
                i = transmit.get(timeout=0.5)
                if i[0] == '.':  # 跳过'.notdef', '.null'
                    continue
                g = self.gs[i]
                pen = ReportLabPen(self.gs, Path())
                g.draw(pen)
                self.g = Group(pen.path)
                d = Drawing(2000, 2000)
                self.g.translate(200, 200)
                d.add(self.g)
                self.imageFile = self.imagePath + "/" + i + ".png"
                renderPM.drawToFile(d, self.imageFile, self.fmt)
                img_name = i + ".png"
                file.put(img_name)
            except:

                break

    def imges_file(self, file: queue.Queue, file_ocr: queue.Queue, file_ocr_name: queue.Queue):
        while True:
            try:
                file_name = file.get(timeout=0.5)
                with open(os.path.join(self.imagePath, file_name), 'rb') as f:
                    file_ocr.put(f.read())
                    file_ocr_name.put(file_name)
            except:
                break

    def text_ocr(self, file_ocr: queue.Queue, file_ocr_name: queue.Queue, statistics: queue.Queue):
        while True:
            try:

                png_b = file_ocr.get(timeout=0.5)
                text_name = file_ocr_name.get(timeout=0.5)
                res = self.ocr.classification(png_b)
                statistics.put({text_name: res})
            except:
                break

    def count(self, statistics: queue.Queue):
        while True:
            if statistics.qsize() == len(self.glyphNames):
                b = {}
                while statistics.qsize():
                    a = statistics.get()
                    for k, v in a.items():
                        b[k] = v
                # statistics.join()
                return b
            else:
                continue

    def run(self):

        self.ttfToImage(self.transmit)

        pool = ThreadPoolExecutor(max_workers=100)

        for i in range(200):
            pool.submit(self.imges_ocr, transmit=self.transmit, file=self.file)
            pool.submit(self.imges_file, file=self.file, file_ocr=self.file_ocr,
                        file_ocr_name=self.file_ocr_name)
            pool.submit(self.text_ocr, file_ocr=self.file_ocr,
                        file_ocr_name=self.file_ocr_name, statistics=self.statistics)

        b = self.count(self.statistics)
        return b



