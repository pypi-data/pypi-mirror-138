from concurrent.futures import ThreadPoolExecutor
import re
import os


class repetition:
    def __init__(self):
        self.white_list = self.read_white_list()

    def remove_repetition(self, texts: list):
        index_texts = [(i, text) for i, text in enumerate(texts)]

        def run_thread(index_text):
            return self.execute(index_text)

        res = []
        # 多线程
        with ThreadPoolExecutor(max_workers=8) as thread_pool:
            # 使用线程执行map计算
            res_text = thread_pool.map(run_thread, index_texts)
            res.extend(res_text)

        return [text[1] for text in sorted(res, key=lambda x: x[0])]

    def execute(self, index_text):
        text = ''
        index = 0
        if isinstance(index_text, tuple):
            text = index_text[1]
            index = index_text[0]

        # 标点与特定字符交换位置
        text = re.sub(r'([，？！。])([呢吗啊吧嘛呀])', r'\2\1', text)

        # 去重 单字叠词 某些特定词不去重
        reg1 = r'([\u4e00-\u9fa5\W]{1}(?!(' + '|'.join(self.white_list) + ')))\\1{1,}'
        text = re.sub(reg1, r"\1", text)

        # 去重 连续的长度为2的重复子串  出现的情况比较多，单独处理
        reg2 = r'([\u4e00-\u9fa5]{2})\1{1,}'
        text = re.sub(reg2, r"\1", text)

        # 去重 重复子串中间间隔4个字以内, 包含连续的重复子串
        reg3 = r'([\u4e00-\u9fa5]{2,})(.{0,4})\1'
        text = re.sub(reg3, r"\1\2", text)

        return (index, text)

    def read_white_list(self):
        path = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件路径的上一级目录
        with open(os.path.join(path, 'white.txt'), 'r') as f:
            while_list = [line.strip() for line in f.readlines()]
            f.close()
        return while_list


if __name__ =='__main__':
    text = '嘛啊如果离地因为咱们湖这边冲的就是地铁二号线，吧##要离地铁的话像一公里一两之内，吧它的你要再超过两公里就有点太远，用不着了对？吧？##对啊一两公里之内那个一两公里之内的话，沿着2号线其实还有10来个楼盘，它那个房价呀##它从远到近吧也是从6000多吧一直到8000多都有，大致就这样一个价位。##6000多是哪里呢？##6000多万就是最近它不间隔，那您看今天不是周末，嘛每周他们开发商会在这个周四周五的时候报一些活动，##但是它只持续两天时间，一般啊到周日的晚上基本就结束了，它会推出30套50套这种特价房给咱们的用户，那我们就会##所以说有时候看房需要很及时的，因为它只有说那么套多套，因为它要多的话，你想啊前期业主买的是蛮贵的对吧？##他要大批量降价的肯定是要维权的对吧？##但是都是有的，6000多的这种还是比较多的，哪些楼盘呢？##啊咱们对那块熟不熟，啊我怕这样给您直接说名字，我说的咱可能是你这字哪些楼盘，##你说就现在这个南龙湖这块是吗？嗯啊你像这个周末的话，你像最近正红的一些房子呀，##包括像正荣的房子一手锁呀都是有所借卖八九千的，现在都有调价，最便宜的都不到7000块钱。'
    rep = repetition()
    print(rep.remove_repetition([text]))