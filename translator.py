from google.cloud import translate
from google.oauth2 import service_account
import json
import six
import os


class Translator(object):
    def __init__(self):
        credentials_raw = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        service_account_info = json.loads(credentials_raw)
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info)
        self._client = translate.Client(credentials=credentials)
        self._text_language = None
        self._target_language = None

    @property
    def text_language(self):
        return self._text_language

    @property
    def target_language(self):
        return self._target_language

    def detect_language(self, text):
            # [START translate_detect_language]
        """Detects the text's language."""

        # Text can also be a sequence of strings, in which case this method
        # will return a sequence of results for each text.
        result = self._client.detect_language(text)

        print('Text: {}'.format(text))
        print('Confidence: {}'.format(result['confidence']))
        print('Language: {}'.format(result['language']))
        self.setup_language(result['language'])
        # [END translate_detect_language]

    def setup_language(self, detected_language):
        self._text_language = detected_language
        target_language = 'ja' if detected_language == 'zh-TW' else 'zh-TW'
        self._target_language = target_language

    def list_languages(self):
        # [START translate_list_codes]
        """Lists all available languages."""

        results = self._client.get_languages()

        for language in results:
            print(u'{name} ({language})'.format(**language))
        # [END translate_list_codes]

    def list_languages_with_target(self, target):
        # [START translate_list_language_names]
        """Lists all available languages and localizes them to the target language.
        Target must be an ISO 639-1 language code.
        See https://g.co/cloud/translate/v2/translate-reference#supported_languages
        """

        results = self._client.get_languages(target_language=target)

        for language in results:
            print(u'{name} ({language})'.format(**language))
        # [END translate_list_language_names]

    def translate_text_with_model(self, target, text, model=translate.NMT):
        # [START translate_text_with_model]
        """Translates text into the target language.
        Make sure your project is whitelisted.
        Target must be an ISO 639-1 language code.
        See https://g.co/cloud/translate/v2/translate-reference#supported_languages
        """

        if isinstance(text, six.binary_type):
            text = text.decode('utf-8')

        # Text can also be a sequence of strings, in which case this method
        # will return a sequence of results for each text.
        result = self._client.translate(
            text, target_language=target, model=model)

        print(u'Text: {}'.format(result['input']))
        print(u'Translation: {}'.format(result['translatedText']))
        print(u'Detected source language: {}'.format(
            result['detectedSourceLanguage']))
        return result['translatedText']
        # [END translate_text_with_model]

    def translate_text(self, target, text):
        # [START translate_translate_text]
        """Translates text into the target language.
        Target must be an ISO 639-1 language code.
        See https://g.co/cloud/translate/v2/translate-reference#supported_languages
        """

        if isinstance(text, six.binary_type):
            text = text.decode('utf-8')

        # Text can also be a sequence of strings, in which case this method
        # will return a sequence of results for each text.
        result = self._client.translate(
            text, target_language=target)

        print(u'Text: {}'.format(result['input']))
        print(u'Translation: {}'.format(result['translatedText']))
        print(u'Detected source language: {}'.format(
            result['detectedSourceLanguage']))
        # [END translate_translate_text]


if __name__ == '__main__':
    trans = Translator()
    result = trans.translate_text_with_model('en', '哈囉 世界')
    print('result is {}'.format(result))
