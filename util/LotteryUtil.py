# -*- coding: utf-8 -*-
import json
import random
from collections import Counter

import requests


class LotteryUtil(object):

    def __init__(self):
        self.url = 'https://www.rundol.com/jtools/lottery/data/findAll'

    def random_ball(self):
        result = []
        response = requests.post(self.url)
        responseJson = response.json().get('data')
        lotteryData = json.loads(responseJson).get('lotteryData')
        lotteryList = list(lotteryData)

        for i in range(len(lotteryList)):
            x = False
            y = False

            base = range(1, 34)
            redBall = random.sample(base, 6)
            redBall.sort()

            red1 = int(lotteryList[i].get('red1'))
            red2 = int(lotteryList[i].get('red2'))
            red3 = int(lotteryList[i].get('red3'))
            red4 = int(lotteryList[i].get('red4'))
            red5 = int(lotteryList[i].get('red5'))
            red6 = int(lotteryList[i].get('red6'))
            his = [red1, red2, red3, red4, red5, red6]

            bits = [redBall[0] % 10, redBall[1] % 10, redBall[2] % 10, redBall[3] % 10, redBall[4] % 10,
                    redBall[5] % 10]
            temp = set(bits)

            if len(bits) == len(temp):
                x = True
            if not ((redBall[0] + 1) == redBall[1] or
                    (redBall[1] + 1) == redBall[2] or
                    (redBall[2] + 1) == redBall[3] or
                    (redBall[3] + 1) == redBall[4] or
                    (redBall[4] + 1) == redBall[5]):
                y = True

            if len(set(his) & set(redBall)) > 3:
                continue
            elif x:
                continue
            elif y:
                continue
            else:
                blueBase = range(1, 16)
                blueBall = random.sample(blueBase, 1)
                redBall.append(blueBall[0])
                result.append(redBall)
                if len(result) == 5:
                    return result


if __name__ == '__main__':
    LotteryUtil().random_ball()
