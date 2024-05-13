from book import ContentType

class Model:
    def make_text_prompt(self, text: str, source_language: str, target_language: str) -> str:
        return f"You are a translation expert, proficient in various languages. \n Translates {source_language} to {target_language}：\n{text}"

    def make_table_prompt(self, table: str, source_language: str, target_language: str) -> str:
        #return f"You are a translation expert, proficient in various languages. \n Translates {source_language} to {target_language}, maintain spacing (spaces, separators) and return in table form：\n{table}"
        return f"You are a translation expert, proficient in various languages. \n Translates {source_language} to {target_language}，maintain in table form：\n{table}"

    def translate_prompt(self, content, source_language: str, target_language: str) -> str:
        if content.content_type == ContentType.TEXT:
            return self.make_text_prompt(content.original, source_language, target_language)
        elif content.content_type == ContentType.TABLE:
            return self.make_table_prompt(content.get_original_as_str(), source_language, target_language)

    def make_request(self, prompt):
        raise NotImplementedError("子类必须实现 make_request 方法")
