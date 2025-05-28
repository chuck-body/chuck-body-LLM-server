from services.speech_service import speech_service
from services.speaker_decision_service import speaker_decision_service
from services.summary_service import summary_service

def merge_text(audio_text):
    result = ""
    for text_frag in audio_text:
        result += f"{text_frag['speaker']}: {text_frag['text']}\n"
    return result

async def audio_to_tags_service(audio_file):
    results = await speech_service(audio_file)
    merged_text = merge_text(results)
    speaker_decied_text = speaker_decision_service(merged_text)
    summary_text = summary_service(speaker_decied_text)
    print(f"summary_text: {summary_text}")
    return summary_text