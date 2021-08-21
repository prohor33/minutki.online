import re


class NERModel():

    theme = re.compile("тема\s*(собрания|встречи|заседания)")
    start_time = re.compile("время начала")
    meeting_initiator = re.compile("инициатор встречи")
    start_participants = re.compile("на[\s]*встреч[\s\w]{1,10}присутст\w+")
    end_participants = re.compile("приступаем к обсуждению")
    start_tasks = re.compile("(по итогам обсуждения)\s*постановил\w*")
    start_task_re = re.compile("(задача|поручение) номер\s\w*\s")
    resposible = re.compile("ответствен\w*")
    date = re.compile("срок")
    end_task_re = re.compile("конец\s(задачи|поручени)")

    def __init__(self) -> None:
        pass

    def run(self, text):
        header = self.get_header(text)
        tasks = self.get_tasks(text)
        return header, tasks


    def get_header(self, text: str) -> dict:
        header = {
            "theme": text[:200],
            "meeting_initiator": "meeting_initiator is not detected",
            "participants": ["participants are not detected"]
        }
        start_theme = re.search(self.theme, text)
        start_date_time = re.search(self.start_time, text)
        start_meeting_initiator = re.search(self.meeting_initiator, text)
        start_participants_pos = re.search(self.start_participants, text)
        end_participants_pos = re.search(self.end_participants, text)

        if start_theme and start_date_time:
            header["theme"] = text[start_theme.end(): start_date_time.start()].strip().capitalize() + "."
        if start_meeting_initiator and start_participants_pos:
            initiator = text[start_meeting_initiator.end(): start_participants_pos.start()].strip()
            header["meeting_initiator"] = " ".join([t.capitalize() for t in initiator.split()]) 
        if start_participants_pos and end_participants_pos:
            particips = text[start_participants_pos.end(): end_participants_pos.start()].strip()
            tokens = particips.split()
            tokens = [t.capitalize() for t in tokens]
            particips = tokens
            if len(tokens) % 2 == 0:
                particips = []
                for i in range(0, len(tokens), 2):
                    particips.append(" ".join(tokens[i: i +2]))

            if len(tokens) % 3 == 0:
                particips = []
                for i in range(0, len(tokens), 3):
                    particips.append(" ".join(tokens[i: i + 2]))

            particips = "; ".join(particips)
            header["participants"] = particips
        for k in header:
            header[k] = self.postprocess_puncts(header[k])
        return header

    def get_tasks(self, text: str) -> dict:
        current_pos = 0
        spans = []
        text_part = text
        while len(text_part) > 1:
            text_part = text[current_pos:]
            match = re.search(self.start_task_re, text_part)
            if not match:
                current_pos += len(text)
                continue
            start_pos = match.end() + current_pos
            end_pos = match.end() + current_pos
            ent_text = text[start_pos:end_pos]
            spans.append(
                (
                    start_pos,
                    end_pos,
                    "n"
                )
            )
            current_pos = end_pos

        tasks = []
        for i_span, span in enumerate(spans):
            if i_span == len(spans) -1:
                tasks.append((span[0], len(text)))
                break
            else:
                tasks.append((span[0], spans[i_span + 1][0] - 1))


        cards = []
        card = {
            "assignment": {"text": "Not defined", "start": 0, "end": 0},
            "responsible": { "text": "Not defined", "start": 0, "end": 0},
            "date": {"text": "Not defined", "start": 0,"end": 0}
        }
        import copy
        for start_task, end_task in tasks:
            resposible_start = re.search(self.resposible, text[start_task:end_task])
            date_start = re.search(self.date, text[start_task:end_task])

            if resposible_start:
                end_pos = start_task + resposible_start.start()
                card["assignment"]["text"] = text[start_task: end_pos].strip().capitalize()
                card["assignment"]["start"] = start_task
                card["assignment"]["end"] = end_pos

            if resposible_start and date_start:
                st_pos = start_task + resposible_start.end()
                end_pos = start_task + date_start.start()
                card["responsible"]["text"] = " ".join([t.capitalize() for t in text[st_pos: end_pos].strip().split()])
                card["responsible"]["start"] = st_pos
                card["responsible"]["end"] = end_pos

            end_tasks_pos = re.search(self.end_task_re, text[start_task:end_task])
            if end_tasks_pos:
                end_task = start_task + end_tasks_pos.start()

            if date_start:
                st_pos = start_task + date_start.end()
                card["date"]["text"] = text[st_pos: end_task].strip().capitalize()
                card["date"]["start"] = st_pos
                card["date"]["end"] = end_task
            new_card = copy.deepcopy(card)
            cards.extend([new_card])
        for card in cards:
            for k in card:
                card[k]["text"] = self.postprocess_puncts(card[k]["text"])
        return cards

    def postprocess_puncts(self, text):
        if text[-1] == ",":
            text = text[:-1]
        if text[0] == ",":
            text = text[1:]
        return text


