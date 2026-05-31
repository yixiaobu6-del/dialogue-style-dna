"""
对话风格DNA提取器 - 风格画像生成
基于分析结果生成综合风格画像
"""

import json
from datetime import datetime


class StyleProfiler:
    """风格画像生成器"""

    def __init__(self, analysis_results: dict):
        """
        初始化画像生成器

        Args:
            analysis_results: 分析结果字典
        """
        self.results = analysis_results

    def generate(self) -> dict:
        """生成完整的风格画像"""
        profile = {
            'basic_info': self._generate_basic_info(),
            'sentence_fingerprint': self._generate_sentence_fingerprint(),
            'vocabulary_dna': self._generate_vocabulary_dna(),
            'rhetoric_signature': self._generate_rhetoric_signature(),
            'tone_personality': self._generate_tone_personality(),
            'style_labels': self._generate_style_labels(),
            'writing_guidelines': self._generate_writing_guidelines()
        }
        return profile

    def _generate_basic_info(self) -> dict:
        """生成基本信息"""
        meta = self.results.get('metadata', {})
        tone = self.results.get('tone', {})
        vocab = self.results.get('vocabulary', {})

        formality = '正式' if tone.get('is_formal', True) else '口语化'

        return {
            'analysis_time': datetime.now().isoformat(),
            'total_texts': meta.get('total_texts', 0),
            'total_sentences': meta.get('total_sentences', 0),
            'vocabulary_richness': vocab.get('type_token_ratio', 0),
            'language_style': formality,
            'overall_complexity': self._calculate_complexity()
        }

    def _calculate_complexity(self) -> str:
        """计算总体复杂度"""
        sentence = self.results.get('sentence_structure', {})
        avg_len = sentence.get('avg_length', 0)
        complex_pct = sentence.get('complex_sentence_pct', 0)
        ttr = self.results.get('vocabulary', {}).get('type_token_ratio', 0)

        complexity_score = (avg_len / 30) * 0.3 + (complex_pct / 50) * 0.3 + ttr * 10 * 0.4

        if complexity_score > 0.7:
            return '高'
        elif complexity_score > 0.4:
            return '中'
        return '低'

    def _generate_sentence_fingerprint(self) -> dict:
        """生成句式指纹"""
        sentence = self.results.get('sentence_structure', {})
        types = sentence.get('sentence_types', {})

        # 句式偏好标签
        preferences = []
        if types.get('interrogative_pct', 0) > 15:
            preferences.append('善用提问')
        if types.get('exclamatory_pct', 0) > 10:
            preferences.append('情感丰富')
        if sentence.get('avg_length', 0) > 20:
            preferences.append('长句为主')
        else:
            preferences.append('短句为主')
        if sentence.get('complex_sentence_pct', 0) > 30:
            preferences.append('句式复杂')

        return {
            'avg_sentence_length': sentence.get('avg_length', 0),
            'sentence_length_std': sentence.get('length_std', 0),
            'length_distribution': sentence.get('length_distribution', {}),
            'declarative_pct': types.get('declarative_pct', 0),
            'interrogative_pct': types.get('interrogative_pct', 0),
            'exclamatory_pct': types.get('exclamatory_pct', 0),
            'complex_sentence_pct': sentence.get('complex_sentence_pct', 0),
            'preferences': preferences
        }

    def _generate_vocabulary_dna(self) -> dict:
        """生成词汇DNA"""
        vocab = self.results.get('vocabulary', {})

        return {
            'vocabulary_size': vocab.get('vocabulary_size', 0),
            'type_token_ratio': vocab.get('type_token_ratio', 0),
            'top_words': vocab.get('top_words', []),
            'keywords': vocab.get('keywords', []),
            'pos_distribution': vocab.get('pos_distribution', {}),
            'common_bigrams': vocab.get('common_bigrams', [])
        }

    def _generate_rhetoric_signature(self) -> dict:
        """生成修辞特征"""
        rhetoric = self.results.get('rhetoric', {})

        signatures = []
        if rhetoric.get('metaphor_count', 0) > 2:
            signatures.append('善用比喻')
        if rhetoric.get('parallelism_count', 0) > 1:
            signatures.append('善用排比')
        if rhetoric.get('rhetorical_question_count', 0) > 2:
            signatures.append('善用反问')
        if rhetoric.get('contrast_count', 0) > 3:
            signatures.append('善用对比')
        if rhetoric.get('quote_count', 0) > 2:
            signatures.append('善用引用')

        return {
            'metaphor_density': rhetoric.get('metaphor_density', 0),
            'parallelism_density': rhetoric.get('parallelism_density', 0),
            'rhetorical_question_count': rhetoric.get('rhetorical_question_count', 0),
            'contrast_count': rhetoric.get('contrast_count', 0),
            'quote_count': rhetoric.get('quote_count', 0),
            'signatures': signatures,
            'dominant_rhetoric': signatures[0] if signatures else '无明显修辞偏好'
        }

    def _generate_tone_personality(self) -> dict:
        """生成语气人格"""
        tone = self.results.get('tone', {})

        # 情感色彩判定
        sentiment = tone.get('sentiment_ratio', 0)
        if sentiment > 0.3:
            emotion_color = '积极乐观'
        elif sentiment < -0.3:
            emotion_color = '审慎批判'
        else:
            emotion_color = '理性中立'

        return {
            'formality': '正式' if tone.get('is_formal', True) else '口语化',
            'informality_score': tone.get('informality_score', 0),
            'sentiment_ratio': tone.get('sentiment_ratio', 0),
            'emotion_color': emotion_color,
            'degree_adverb_density': tone.get('adverb_density', 0),
            'first_person_density': tone.get('first_person_density', 0),
            'common_modal_particles': {
                k: v for k, v in tone.get('modal_particles', {}).items()
                if v > 0
            }
        }

    def _generate_style_labels(self) -> list:
        """生成风格标签"""
        labels = []
        tone = self.results.get('tone', {})
        sentence = self.results.get('sentence_structure', {})
        rhetoric = self.results.get('rhetoric', {})

        # 根据特征添加标签
        if tone.get('is_formal', True):
            labels.append('正式严谨')
        else:
            labels.append('亲切自然')

        if sentence.get('avg_length', 0) > 20:
            labels.append('深度阐述')
        else:
            labels.append('简洁明了')

        if rhetoric.get('metaphor_count', 0) > 2:
            labels.append('形象生动')

        if rhetoric.get('rhetorical_question_count', 0) > 2:
            labels.append('善于引导')

        if tone.get('sentiment_ratio', 0) > 0.2:
            labels.append('积极正向')

        return labels

    def _generate_writing_guidelines(self) -> list:
        """生成写作指导建议"""
        guidelines = []

        sentence = self.results.get('sentence_structure', {})
        avg_len = sentence.get('avg_length', 0)
        types = sentence.get('sentence_types', {})

        # 句式建议
        if avg_len > 25:
            guidelines.append("适当地插入短句，可以增强语言的节奏感")
        elif avg_len < 12:
            guidelines.append("可以尝试增加复合句，丰富表达的层次感")

        if types.get('interrogative_pct', 0) < 5:
            guidelines.append("适当增加提问，可以增强与读者的互动感")

        # 词汇建议
        ttr = self.results.get('vocabulary', {}).get('type_token_ratio', 0)
        if ttr < 0.3:
            guidelines.append("尝试增加词汇多样性，避免重复使用相同的表达方式")

        # 修辞建议
        rhetoric = self.results.get('rhetoric', {})
        if rhetoric.get('metaphor_count', 0) < 2:
            guidelines.append("适当使用比喻可以让抽象概念变得更生动")

        if rhetoric.get('parallelism_count', 0) < 1:
            guidelines.append("排比句可以增强语势和说服力")

        # 语气建议
        tone = self.results.get('tone', {})
        if tone.get('is_formal', True):
            guidelines.append("在适当场合可以增加语气词，让表达更亲切")

        return guidelines

    def generate_report(self) -> str:
        """生成可读的报告文本"""
        profile = self.generate()

        report = []
        report.append("=" * 60)
        report.append("对话风格DNA提取报告")
        report.append("=" * 60)
        report.append("")

        # 基本信息
        info = profile['basic_info']
        report.append("[基本信息]")
        report.append(f"  分析文本量: {info['total_sentences']} 句")
        report.append(f"  语言风格: {info['language_style']}")
        report.append(f"  表达复杂度: {info['overall_complexity']}")
        report.append("")

        # 风格标签
        report.append("[风格标签]")
        for label in profile['style_labels']:
            report.append(f"  #{label}")
        report.append("")

        # 句式指纹
        sf = profile['sentence_fingerprint']
        report.append("[句式指纹]")
        report.append(f"  平均句长: {sf['avg_sentence_length']:.1f} 字")
        report.append(f"  陈述句占比: {sf['declarative_pct']}%")
        report.append(f"  疑问句占比: {sf['interrogative_pct']}%")
        report.append(f"  感叹句占比: {sf['exclamatory_pct']}%")
        report.append(f"  偏好特征: {', '.join(sf['preferences'])}")
        report.append("")

        # 修辞特征
        rs = profile['rhetoric_signature']
        report.append("[修辞特征]")
        report.append(f"  比喻密度: {rs['metaphor_density']:.3f}")
        report.append(f"  排比密度: {rs['parallelism_density']:.3f}")
        report.append(f"  主要修辞风格: {rs['dominant_rhetoric']}")
        report.append("")

        # 语气人格
        tp = profile['tone_personality']
        report.append("[语气人格]")
        report.append(f"  正式程度: {tp['formality']}")
        report.append(f"  情感色彩: {tp['emotion_color']}")
        report.append(f"  情感倾向: {tp['sentiment_ratio']:.3f}")
        report.append("")

        # 写作建议
        report.append("[写作建议]")
        for i, guideline in enumerate(profile['writing_guidelines'], 1):
            report.append(f"  {i}. {guideline}")
        report.append("")
        report.append("=" * 60)

        return '\n'.join(report)

    def save_report(self, output_path: str) -> None:
        """保存报告"""
        profile = self.generate()

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(profile, f, ensure_ascii=False, indent=2)

        print(f"风格画像已保存至: {output_path}")


if __name__ == '__main__':
    # 示例用法
    from .analyzer import StyleAnalyzer

    analyzer = StyleAnalyzer()
    analyzer.load_texts([
        "我认为，AI技术虽然发展迅速，但人类始终是决策的核心。"
        "机器可以帮助我们分析数据、提供建议，但最终的判断应该由人来做。"
        "这不是技术能力问题，而是伦理责任问题。你说对吗？"
    ])
    results = analyzer.analyze()

    profiler = StyleProfiler(results)
    print(profiler.generate_report())