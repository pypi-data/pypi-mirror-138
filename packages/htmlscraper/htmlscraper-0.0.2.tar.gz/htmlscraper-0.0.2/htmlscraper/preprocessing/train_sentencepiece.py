import io

import sentencepiece as spm


def train(sentence_iterator, path,
          model_type='unigram',
          vocab_size=2000,
          character_coverage=0.9995,
          required_chars=None,
          user_defined_symbols=None,
          max_sentencepiece_length=16,
          byte_fallback=False,
          split_digits=True):
    if user_defined_symbols is None:
        user_defined_symbols = ['<sep>', '<cls>']

    model = io.BytesIO()

    spm.SentencePieceTrainer.Train(sentence_iterator=sentence_iterator,
                                   model_writer=model,
                                   model_type=model_type,
                                   vocab_size=vocab_size,
                                   character_coverage=character_coverage,
                                   required_chars=required_chars,
                                   user_defined_symbols=user_defined_symbols,
                                   max_sentencepiece_length=max_sentencepiece_length,
                                   byte_fallback=byte_fallback,
                                   split_digits=split_digits)

    with open(path, 'wb') as f:
        f.write(model.getvalue())

