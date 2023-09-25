from dotenv import load_dotenv
import os
import requests
import wave

# Import namespaces
import azure.cognitiveservices.speech as speech_sdk
from playsound import playsound
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, ResultReason
import wavio

# Define speech configuration globally
speech_config = SpeechConfig("51b7db38f9c84ac98df4334cf8bea574", "eastus")
targetLanguage = 'ur'

def main():
    try:
        global speech_config
        global translation_config

        # Get Configuration Settings
        load_dotenv()
        cog_key = os.getenv('COG_SERVICE_KEY')
        cog_region = os.getenv('COG_SERVICE_REGION')

        # Configure translation
        translation_config = speech_sdk.translation.SpeechTranslationConfig(cog_key, cog_region)
        translation_config.speech_recognition_language = 'en-US'
        translation_config.add_target_language('ur')
        print('Ready to translate from',translation_config.speech_recognition_language)

        # Configure speech service
        speech_config = speech_sdk.SpeechConfig(cog_key, cog_region)
        print('Ready to use speech service in:', speech_config.region)

        # Get spoken input
        command = TranscribeCommand()

    except Exception as ex:
        print(ex)

def TranscribeCommand():
    command = ''

    # Configure speech recognition
    audio_config = speech_sdk.AudioConfig(filename="Faiza_Ali_intro.wav") 
    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)

    # Process speech input
    speech = speech_recognizer.recognize_once_async().get()
    if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
        command = speech.text
        print(command)
        
        def FaizaCall():
        # Configure speech recognition
            audio_config = speech_sdk.AudioConfig(filename="Faiza_Ali_intro.wav") 
            speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)

         # Process speech input
            speech = speech_recognizer.recognize_once_async().get()
            if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
                recognized_text = speech.text
                print("Recognized:", recognized_text)
        
                # Check if your name is in the recognized text
                ## here in my recording it detected Faisal intead of Faiza so i have placed Faisal for name recognition
                if "Faisal" in recognized_text:
                    print("Congratulations! Your name was recognized!")
                    def TellName():
                        response_text = 'my name is Faisal Ali.'

                        # Configure speech synthesis
                        speech_config.speech_synthesis_voice_name = 'en-GB-LibbyNeural'
                        speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)

                        # Synthesize spoken output
                        responseSsml = " \
                        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'> \
                        <voice name='en-GB-LibbyNeural'> \
                        {} \
                                <break strength='weak'/> \
                                    Nice to meet you! \
                                        </voice> \
                                    </speak>".format(response_text)
                        speak = speech_synthesizer.speak_ssml_async(responseSsml).get()
                        if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
                            print(speak.reason)

                        # Call the TellName function to announce your name
                    TellName()

                    def Translate_voice():
                        response_text = 'میرا نام فائزہ علی ہے'

                        # Configure speech synthesis
                        speech_config.speech_synthesis_voice_name = 'ur-IN-SalmanNeural' # change this
                        speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)

                        # Synthesize spoken output
                        responseSsml = " \
                        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='ur-IN'> \
                        <voice name='ur-IN-SalmanNeural'> \
                        {} \
                                <break strength='weak'/> \
                                    آپ سے مل کر خوشی ہوئی! \
                                        </voice> \
                                    </speak>".format(response_text)
                        speak = speech_synthesizer.speak_ssml_async(responseSsml).get()
                        if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
                            print(speak.reason)                 
                    targetLanguage = ''
                    while targetLanguage != 'quit':
                        targetLanguage = input('\nEnter a target language\n ur=urdu\n Enter anything else to stop\n').lower()
                        if targetLanguage in translation_config.target_languages:
                            Translate(targetLanguage)
                        else:
                            targetLanguage = 'quit'
                else:
                     print("Oooo, Sorry Your name was not recognized.")
            else:
                print("Speech recognition failed.")

        # Call the function
        FaizaCall()
    else:
        print(speech.reason)
        if speech.reason == speech_sdk.ResultReason.Canceled:
            cancellation = speech.cancellation_details
            print(cancellation.reason)
            print(cancellation.error_details)

    # Return the command
    return command

#     print(response_text)
def Translate(targetLanguage):
    translation = ''

    # Translate speech
    audioFile = 'Faiza_Ali_intro.wav'
    playsound(audioFile)
    audio_config = speech_sdk.AudioConfig(filename=audioFile)
    translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config = audio_config)
    print("Please wait, we are getting speech from file...")
    result = translator.recognize_once_async().get()
    print('Translating "{}"'.format(result.text))
    translation = result.translations[targetLanguage]
    print(translation)

    # urdu text to voice (Text to Speech)             
def Translate_voice(translation):
    response_text = translation

    # Configure speech synthesis
    speech_config.speech_synthesis_voice_name = 'ur-IN-SalmanNeural' 
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)

    # Synthesize spoken output
    responseSsml = f" \
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='ur-IN'> \
        <voice name='ur-IN-SalmanNeural'> \
            {response_text} \
            <break strength='weak'/> \
            آپ سے مل کر خوشی ہوئی! \
        </voice> \
        </speak>"
    
    audio_data = speech_synthesizer.speak_ssml_async(responseSsml).get()
    if audio_data.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(audio_data.reason)
        return

    # Save the audio to a WAV file
    with open("translation.wav", "wb") as wav_file:
        wav_file.write(audio_data.audio_data)

    # Synthesize translation
    voices ={ "ur": "ur-UR"}
    speech_config.speech_synthesis_voice_name = voices.get(targetLanguage)
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)
    speak = speech_synthesizer.speak_text_async(translation).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)


# Call the translate function
if __name__ == "__main__":
    main()
