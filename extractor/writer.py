"""
对话风格DNA提取器 - 风格模仿写作器
基于风格画像生成风格一致的文本
"""

import json
import random
import re
from pathlib import Path


class StyleWriter:
    """风格模仿写作器"""

    def __init__(self, profile_path: str):
        """
        初始化写作器

        Args:
            profile_path: 风格画像文件路径
        """
        with open(profile_path, 'r', encoding='utf-8') as f:
            self.profile = json.load(f)

        self._init_writing_rules()

    def _init_writing_rules(self):
        """从画像生成写作规则"""
        sf = self.profile.get('sentence_fingerprint', {})
        tp = self.profile.get('tone_personality', {})
        vd = self.profile.get('vocabulary_dna', {})
        rs = self.profile.get('rhetoric_signature', {})

        self.rules = {
            'target_sentence_length': sf.get('avg_sentence_length', 20),
            'target_complexity': sf.get('complex_sentence_pct', 20),
            'interrogative_pct': sf.get('interrogative_pct', 10),
            'exclamatory_pct': sf.get('exclamatory_pct', 5),
            'formality': tp.get('formality', '正式'),
            'emotion_color': tp.get('emotion_color', '理性中立'),
            'top_words': [w['word'] for w in vd.get('top_words', [])[:10]],
            'dominant_rhetoric': rs.get('dominant_rhetoric', ''),
            'use_metaphor': '善用比喻' in rs.get('signatures', []),
            'use_parallelism': '善用排比' in rs.get('signatures', []),
            'use_rhetorical_question': '善用反问' in rs.get('signatures', []),
        }

    def write(self, topic: str) -> str:
        """
        模拟风格写作

        Args:
            topic: 写作主题

        Returns:
            生成文本
        """
        paragraphs = []
        paragraphs.append(self._generate_opening(topic))
        paragraphs.append(self._generate_body(topic))
        paragraphs.append(self._generate_closing(topic))

        text = '\n\n'.join(paragraphs)
        text = self._apply_style_transforms(text)

        return text

    def _generate_opening(self, topic: str) -> str:
        """生成开头段落"""
        openings = [
            f"关于{topic}这个话题，值得我们深入探讨。",
            f"谈到{topic}，我想从另一个角度来分析。",
            f"{topic}是当下很多人都在关注的问题，我有几点想法。",
        ]

        if self.rules['interrogative_pct'] > 10:
            openings.append(f"你有没有思考过{topic}背后的深层逻辑？")

        return random.choice(openings)

    def _generate_body(self, topic: str) -> str:
        """生成主体段落"""
        body_parts = []

        # 核心观点
        viewpoints = [
            f"首先需要明确的是，{topic}不是一个简单的非黑即白的问题。",
            f"从多个维度来看，{topic}涉及到技术、人文和社会的交织。",
            f"{topic}的核心在于，如何在效率和安全之间找到平衡。",
        ]

        body_parts.append(random.choice(viewpoints))

        # 展开论述
        if self.rules['use_metaphor']:
            metaphors = [
                f"这就像一把双刃剑，既带来了便利，也伴随着风险。",
                f"如同航行在未知海域，机遇与挑战并存。",
            ]
            body_parts.append(random.choice(metaphors))

        # 逻辑推进
        body_parts.append(f"一方面，{topic}为我们打开了新的可能性。")
        body_parts.append(f"另一方面，我们也不能忽视其中存在的问题和挑战。")

        # 举例
        body_parts.append(f"举个具体的例子，在实际应用中，{topic}已经展现出巨大的潜力。")

        if self.rules['use_rhetorical_question']:
            body_parts.append(f"难道这不是一个值得我们深入思考的议题吗？")

        return ' '.join(body_parts)

    def _generate_closing(self, topic: str) -> str:
        """生成结尾段落"""
        closings = [
            f"总的来说，{topic}是一个需要持续关注的议题，我们需要在实践中不断调整和完善。",
            f"关于{topic}，我的观点是：保持开放的心态，同时也要保持理性的判断。",
            f"{topic}的未来走向，取决于我们如何从现在开始做出明智的选择。",
        ]
        return random.choice(closings)

    def _apply_style_transforms(self, text: str) -> str:
        """应用风格转换"""
        # 句式长度调整
        if self.rules['target_sentence_length'] > 20:
            text = self._lengthen_sentences(text)
        else:
            text = self._shorten_sentences(text)

        # 添加语气词（如果是口语化风格）
        if not self.rules['formality'] == '正式':
            text = self._add_modal_particles(text)

        # 添加排比
        if self.rules['use_parallelism']:
            text = self._add_parallelism(text)

        # 融入高频词
        if self.rules['top_words']:
            text = self._inject_vocabulary(text)

        return text

    def _lengthen_sentences(self, text: str) -> str:
        """增长句子"""
        sentences = re.split(r'([。！？])', text)
        result = []
        i = 0

        while i < len(sentences) - 1:
            if i + 2 < len(sentences) and random.random() < 0.3:
                combined = sentences[i] + '，' + sentences[i + 2]
                result.append(combined + sentences[i + 1])
                i += 3
            else:
                result.append(sentences[i] + sentences[i + 1])
                i += 2

        if i < len(sentences):
            result.append(sentences[i])

        return ''.join(result)

    def _shorten_sentences(self, text: str) -> str:
        """缩短句子"""
        # 在长句中插入断句
        text = re.sub(r'([^。！？]{30,40})([，,])', r'\1。\2', text)
        return text

    def _add_modal_particles(self, text: str) -> str:
        """添加语气词"""
        particles = ['啊', '吧', '呢', '哦', '嘛']
        count = max(1, len(text) // 100)

        for _ in range(count):
            pos = random.randint(len(text) // 4, len(text) * 3 // 4)
            particle = random.choice(particles)
            text = text[:pos] + particle + text[pos:]

        return text

    def _add_parallelism(self, text: str) -> str:
        """添加排比句式"""
        patterns = [
            f"没有充分的准备，没有深入的调研，没有缜密的规划，任何项目都难以成功。",
        ]
        if random.random() < 0.3:
            text = text.rstrip('。') + '。' + random.choice(patterns)

        return text

    def _inject_vocabulary(self, text: str) -> str:
        """注入高频词汇"""
        words_to_inject = [w for w in self.rules['top_words'] if len(w) > 1]

        if words_to_inject and random.random() < 0.5:
            word = random.choice(words_to_inject)
            text = text.replace('方面', f'{word}方面', 1)

        return text

    def write_batch(self, topics: list) -> list:
        """批量写作"""
        return [self.write(topic) for topic in topics]


class StyleMixer:
    """风格混合器 - 融合多种风格"""

    def __init__(self, profile_paths: list):
        """
        初始化混合器

        Args:
            profile_paths: 多个风格画像路径
        """
        self.writers = [StyleWriter(path) for path in profile_paths]

    def mix(self, topic: str, weights: list = None) -> str:
        """
        混合多种风格写作

        Args:
            topic: 主题
            weights: 各风格权重

        Returns:
            混合风格文本
        """
        if not weights:
            weights = [1.0 / len(self.writers)] * len(self.writers)

        texts = [writer.write(topic) for writer in self.writers]

        # 按权重选择句子组成混合文本
        all_sentences = []
        for text, weight in zip(texts, weights):
            sentences = re.split(r'([。！？])', text)
            pairs = [(sentences[i], sentences[i + 1]) for i in range(0, len(sentences) - 1, 2)]
            count = max(1, int(len(pairs) * weight))
            all_sentences.extend(random.sample(pairs, min(count, len(pairs))))

        random.shuffle(all_sentences)
        return ''.join(s + p for s, p in all_sentences)

    def create_hybrid_profile(self, weights: list = None, output_path: str = '') -> dict:
        """创建混合风格画像"""
        if not weights:
            weights = [1.0 / len(self.writers)] * len(self.writers)

        profiles = [w.profile for w in self.writers]
        hybrid = {}

        # 加权平均数值型特征
        for key in profiles[0]:
            if isinstance(profiles[0][key], (int, float)):
                hybrid[key] = sum(p[key] * w for p, w in zip(profiles, weights))
            elif isinstance(profiles[0][key], list):
                hybrid[key] = list(set().union(*[p[key] for p in profiles]))
            elif isinstance(profiles[0][key], dict):
                hybrid[key] = profiles[0][key]

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(hybrid, f, ensure_ascii=False, indent=2)

        return hybrid


if __name__ == '__main__':
    # 示例用法（需要先有画像文件）
    print("风格模仿写作器 - 需要先通过 analyzer 和 profile 生成画像文件")
    print("示例: writer = StyleWriter('style_profile.json')")
    print("       result = writer.write('人工智能的未来')")