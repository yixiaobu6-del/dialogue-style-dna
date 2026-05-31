"""
对话风格DNA提取器 - 风格分析核心模块
负责句式分析、高频词统计、修辞识别
"""

import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Optional

import jieba
import jieba.analyse


class StyleAnalyzer:
    """风格分析器，提取文本多维特征"""

    def __init__(self):
        """初始化分析器"""
        self.texts: list = []
        self.sentences: list = []
        self.words: list = []
        self.results = {}

    def load_texts(self, texts: list) -> None:
        """加载待分析文本"""
        self.texts = texts
        # 分句
        self.sentences = []
        for text in texts:
            parts = re.split(r'[。！？；\n]', text)
            self.sentences.extend([s.strip() for s in parts if len(s.strip()) > 2])

        # 分词
        all_text = ' '.join(texts)
        self.words = jieba.lcut(all_text)

    def load_from_file(self, file_path: str) -> None:
        """从文件加载文本"""
        path = Path(file_path)

        if path.suffix == '.json':
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    texts = [item.get('content', '') for item in data]
                else:
                    texts = [data.get('content', '')]
            self.load_texts(texts)

        elif path.suffix in ('.txt', '.md'):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
            self.load_texts(paragraphs)

    def analyze_sentence_structure(self) -> dict:
        """分析句式结构"""
        if not self.sentences:
            return {}

        lengths = [len(s) for s in self.sentences]
        avg_length = sum(lengths) / len(lengths)

        # 计算标准差
        variance = sum((l - avg_length) ** 2 for l in lengths) / len(lengths)
        std = math.sqrt(variance)

        # 句长分布
        length_distribution = defaultdict(int)
        for l in lengths:
            if l <= 10:
                length_distribution['short(1-10)'] += 1
            elif l <= 20:
                length_distribution['medium(11-20)'] += 1
            elif l <= 30:
                length_distribution['long(21-30)'] += 1
            else:
                length_distribution['very_long(31+)'] += 1

        # 句子类型分析
        decl_count = 0      # 陈述句
        interrog_count = 0  # 疑问句
        exclam_count = 0    # 感叹句
        dash_count = 0      # 破折号
        colon_count = 0     # 冒号

        for s in self.sentences:
            if '？' in s or '?' in s:
                interrog_count += 1
            elif '！' in s or '!' in s:
                exclam_count += 1
            else:
                decl_count += 1

        # 复杂句式检测
        complex_count = 0
        for s in self.sentences:
            clauses = re.split(r'[，,；;、]', s)
            if len(clauses) >= 3:
                complex_count += 1

        # 标点符号统计
        all_text = ''.join(self.texts)
        for c in all_text:
            if c == '——':
                dash_count += 1
            elif c == '：':
                colon_count += 1

        total_chars = len(all_text) if all_text else 1

        return {
            'sentence_count': len(self.sentences),
            'avg_length': round(avg_length, 2),
            'length_std': round(std, 2),
            'length_distribution': dict(length_distribution),
            'sentence_types': {
                'declarative_pct': round(decl_count / len(self.sentences) * 100, 1),
                'interrogative_pct': round(interrog_count / len(self.sentences) * 100, 1),
                'exclamatory_pct': round(exclam_count / len(self.sentences) * 100, 1),
            },
            'complex_sentence_pct': round(complex_count / len(self.sentences) * 100, 1),
            'punctuation_density': {
                'dash_per_1000': round(dash_count / total_chars * 1000, 2),
                'colon_per_1000': round(colon_count / total_chars * 1000, 2),
            }
        }

    def analyze_vocabulary(self) -> dict:
        """分析词汇使用特征"""
        if not self.words:
            return {}

        # 过滤停用词和单字词
        stopwords = {'的', '了', '是', '在', '我', '有', '和', '就', '不', '人',
                     '都', '一', '个', '上', '也', '很', '到', '说', '要', '去',
                     '这', '那', '你', '他', '她', '它', '们', '与', '为', '之'}
        filtered_words = [w for w in self.words if len(w) > 1 and w not in stopwords]

        # 词频统计
        word_freq = Counter(filtered_words)
        top_words = word_freq.most_common(30)

        # 词汇丰富度（类符形符比）
        types = len(set(filtered_words))
        tokens = len(filtered_words)
        ttr = types / tokens if tokens > 0 else 0

        # 关键词提取（基于TF-IDF）
        all_text = ' '.join(self.texts)
        keywords = jieba.analyse.extract_tags(all_text, topK=20)

        # 词性分析（统计名词、动词、形容词比例）
        pos_tags = jieba.posseg.cut(all_text)
        pos_counts = Counter()
        for word, flag in pos_tags:
            if len(word) > 1:
                pos_counts[flag] += 1

        total_pos = sum(pos_counts.values()) or 1

        # 高频表达模式
        pattern_counts = Counter()
        for i in range(len(self.words) - 1):
            bigram = self.words[i] + self.words[i + 1]
            if len(bigram) >= 3 and not any(c in bigram for c in '，。！？、；：'):
                pattern_counts[bigram] += 1

        common_patterns = [p for p, c in pattern_counts.most_common(15) if c >= 2]

        return {
            'vocabulary_size': types,
            'total_tokens': tokens,
            'type_token_ratio': round(ttr, 4),
            'top_words': [{'word': w, 'count': c} for w, c in top_words[:20]],
            'keywords': keywords,
            'pos_distribution': {
                'noun_pct': round(pos_counts.get('n', 0) / total_pos * 100, 1),
                'verb_pct': round(pos_counts.get('v', 0) / total_pos * 100, 1),
                'adj_pct': round(pos_counts.get('a', 0) / total_pos * 100, 1),
                'adv_pct': round(pos_counts.get('d', 0) / total_pos * 100, 1),
            },
            'common_bigrams': common_patterns[:10]
        }

    def analyze_rhetoric(self) -> dict:
        """识别修辞手法"""
        if not self.texts:
            return {}

        all_text = ' '.join(self.texts)

        # 排比检测
        parallelism_patterns = [
            r'(.{3,10})[，,]\1',       # ABCD, ABCD
            r'(没有.{2,10}[，,]\s*){3,}',  # 没有...，没有...，没有...
            r'(要.{2,10}[，,]\s*){3,}',   # 要...，要...，要...
            r'(让.{2,10}[，,]\s*){3,}',   # 让...，让...，让...
        ]

        parallelism_count = 0
        for pattern in parallelism_patterns:
            matches = re.findall(pattern, all_text)
            parallelism_count += len(matches)

        # 比喻检测
        metaphor_words = ['像', '如同', '好比', '仿佛', '似', '宛如', '犹如', '跟...一样']
        metaphor_count = sum(
            len(re.findall(f"{word}", all_text))
            for word in ['像', '如同', '好比', '仿佛', '宛如', '犹如']
        )

        # 反问检测
        rhetorical_questions = re.findall(r'(难道|岂|何尝|何必|何不)', all_text)

        # 设问检测（自问自答）
        qa_pattern = re.findall(r'([^。！？]*[？?][^。！？]*[。])', all_text)

        # 对比修辞
        contrast_patterns = re.findall(r'(虽然.{2,15}但|然而.{2,15}|不过.{2,15}|却|反之|相反)', all_text)

        # 引用检测
        quote_patterns = re.findall(r'["""]([^"""]+)["""]', all_text)

        # 排比句检测
        parallel_sentences = re.findall(r'(.{10,40}[，,])\s*(.{10,40}[，,])\s*(.{10,40}[。！？])', all_text)

        return {
            'parallelism_count': parallelism_count,
            'parallelism_density': round(parallelism_count / len(self.sentences), 4) if self.sentences else 0,
            'metaphor_count': metaphor_count,
            'metaphor_density': round(metaphor_count / len(self.sentences), 4) if self.sentences else 0,
            'rhetorical_question_count': len(rhetorical_questions),
            'self_qa_count': len(qa_pattern),
            'contrast_count': len(contrast_patterns),
            'quote_count': len(quote_patterns),
            'parallel_sentence_groups': len(parallel_sentences),
        }

    def analyze_tone(self) -> dict:
        """分析语气特征"""
        if not self.texts:
            return {}

        all_text = ' '.join(self.texts)
        total_chars = len(all_text) if all_text else 1

        # 语气词检测
        modal_particles = {
            '啊': 0, '吧': 0, '呢': 0, '吗': 0, '嘛': 0, '哦': 0,
            '嗯': 0, '哎': 0, '唉': 0, '哟': 0, '哈': 0, '啦': 0,
        }
        for word in modal_particles:
            modal_particles[word] = all_text.count(word)

        total_particles = sum(modal_particles.values())

        # 程度副词
        degree_adverbs = [
            '非常', '很', '太', '极其', '特别', '相当', '十分',
            '比较', '稍微', '略微', '有点', '有些', '颇为'
        ]
        adverb_count = sum(all_text.count(adv) for adv in degree_adverbs)

        # 情感词汇
        positive_words = ['喜欢', '开心', '高兴', '满意', '期待', '希望', '爱', '好', '棒', '优秀', '精彩']
        negative_words = ['讨厌', '难过', '伤心', '失望', '担心', '害怕', '恨', '差', '糟', '糟糕', '失败']

        pos_count = sum(all_text.count(w) for w in positive_words)
        neg_count = sum(all_text.count(w) for w in negative_words)

        # 口语化程度（基于语气词比例）
        informality_score = total_particles / (len(self.sentences) + 1)

        # 情感倾向
        total_emotion = pos_count + neg_count
        sentiment_ratio = (pos_count - neg_count) / total_emotion if total_emotion > 0 else 0

        # 第一人称使用频率
        first_person_count = all_text.count('我') + all_text.count('我们')
        first_person_density = first_person_count / total_chars * 100

        return {
            'modal_particles': modal_particles,
            'total_modal_particles': total_particles,
            'modal_particle_density': round(total_particles / total_chars * 100, 3),
            'degree_adverb_count': adverb_count,
            'adverb_density': round(adverb_count / total_chars * 100, 3),
            'positive_word_count': pos_count,
            'negative_word_count': neg_count,
            'sentiment_ratio': round(sentiment_ratio, 3),
            'informality_score': round(informality_score, 3),
            'first_person_density': round(first_person_density, 3),
            'is_formal': informality_score < 0.1
        }

    def analyze(self) -> dict:
        """执行完整分析"""
        self.results = {
            'sentence_structure': self.analyze_sentence_structure(),
            'vocabulary': self.analyze_vocabulary(),
            'rhetoric': self.analyze_rhetoric(),
            'tone': self.analyze_tone(),
            'metadata': {
                'total_texts': len(self.texts),
                'total_sentences': len(self.sentences),
                'total_words': len(self.words),
            }
        }
        return self.results


if __name__ == '__main__':
    # 示例用法
    sample_texts = [
        "你好，我想和你聊聊天于人工智能的话题。人工智能真的很有趣，它正在改变我们的生活方式。",
        "但是，我们也要警惕AI带来的风险。比如数据隐私和就业替代问题。你觉得呢？",
        "我认为，最好的方式是找到平衡点。既不要过度恐惧，也不要盲目乐观。我们需要理性看待AI的发展。",
        "从历史上看，每一次技术革命都会带来阵痛，但最终都会让人类受益。蒸汽机、电力、互联网都是这样。",
    ]

    analyzer = StyleAnalyzer()
    analyzer.load_texts(sample_texts)
    results = analyzer.analyze()
    print(json.dumps(results, ensure_ascii=False, indent=2))