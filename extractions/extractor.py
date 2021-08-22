from natasha import NamesExtractor
from rutermextract import TermExtractor


def get_span_names(sample_text):
    names_extractor = NamesExtractor()
    filtered_spans = []
    matches = names_extractor(" ".join([token.capitalize() for token in sample_text.split()]))
    for match in matches:
        if match.fact.first and match.fact.last and len(match.fact.last) > 2 and len(match.fact.first) > 3:
            filtered_spans.append((match.span[0], match.span[1] + 1, "ФИО"))
    return filtered_spans


def get_summary(sample_text):
    extracted_words = []
    term_extractor = TermExtractor()
    for term in term_extractor(sample_text):
        extracted_words.extend([word.parsed.word for word in term.words])

    tokens = sample_text.split()
    tokens_position = []
    current_pos = 0
    for token in sample_text.split():
        end_pos = current_pos + len(token)
        tokens_position.append((current_pos, end_pos))
        current_pos = end_pos + 1

    index_kw_tokens = [0] * len(tokens)
    for i_token, token in enumerate(tokens):
        if token in extracted_words:
            index_kw_tokens[i_token] = 1

    bound = 100
    distibution = []
    for i in range(0, len(index_kw_tokens), 50):
        distibution.append((i, i + bound, sum(index_kw_tokens[i: i + bound])))

    distibution = sorted(distibution, key=lambda x: x[-1], reverse=True)
    spans = []
    n_span = 10
    for sample in distibution[:n_span]:
        star_token_index, end_token_index, n_tokens = sample
        start_span = tokens_position[star_token_index][0]
        end_span = tokens_position[end_token_index][-1]
        spans.append((start_span, end_span, "KWE_span"))

    needed_distr = sorted(spans, key=lambda x: x[0], reverse=False)
    formatted_spans = []
    current_span = None
    for span in needed_distr:
        if current_span is None:
            current_span = span
            continue
        if current_span[0] <= span[1] <= current_span[1]:
            current_span = (current_span[0], span[1], span[-1])
        else:
            formatted_spans.append(current_span)
            current_span = span
    return formatted_spans
