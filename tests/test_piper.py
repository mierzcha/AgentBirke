from src.tts.piper_client import PiperClient

client = PiperClient(model_path="models/piper/de_DE-ramona-low.onnx")
output_path = client.generate(text="Hallo, ich bin Agent Birke.",output_filename="test_piper_client_output.wav",)
print(f"Audio 1 gespeichert unter: {output_path}")
output_path = client.generate(
    text="""Hallo zusammen,
Leider gibt es immer noch ein paar Leute die auf Rechtschreibung scheißen. Wir haben heute einen ganz besonderen Lehrer, der diesen Leuten einen Crashkurs verpasst. Begrüßen wir ihn zusammen...
Guten Morgen Herr Macklemore.

Alright Okay 
Alright Okay... Schluss mit dem Stuss

Ich guck auf meinen Mac, Comments abgecheckt, und direkt den Unsinn aufgedeckt.
Vieles schreibt man wie man's spricht, Unsinn aber nicht. Das muss groß und mit zwei „n". 
Oh man - so geht das nicht. Egal ob Hater oder Fan. Hier schreibt jemand „ihr seid so dumm." 
Man rend nicht auf der Straße rum. Aber rennt bitte mit „t" und zwei „n". Wer ist hier dumm? 
Oh man - weg vom Mac. Ich zeig wie's geht, mit diesem Track, damit ihr seht, kein Geschwätz - hört alle her, 
Rechtschreibung ist gar nicht schwer. Fangen wir an mit'n paar Tricks - das geht fix - und kost' nix. 
Wer nämlich mit „h" schreibt ist dämlich. Genauso wie ziemlich und dämlich. Also seid nicht dämlich - lasst das „h" raus. 
Und hört endlich auf zu schwätzen - auch du Klaus. 
Trenne nie das "s" vom "t", denn das tut beiden weh. Bei seit gehts um die Zeit. Betonung auf „t" - Hände weg vom „d". 
Dieser Hater fühlt sich gerade sehr durchtrieben. Doch ich muss ihm sagen, gar nicht wird gar nicht zusammen geschrieben. 
Depp. Seid ihr auch in Englisch fit? He, she, it - „s" muss mit. He, she, it mit „s" is' fit. Sprecht jetzt alle mit: A B C D E F G H I K L M N O P Q R S T U V W. Das war das ganze ABC.

Äh ne, du hast das was vergessen, Meck

Wie bitte? SETZEN 6!

Macklemore lehrt euch Kommentare zu schreiben, denn so wie es ist, kann es leider nicht bleiben. Egal ob ein Fan oder übelster Hater, achte auf Rechtschreibung und mach' keine Fehler. 
    """,
    output_filename="test_piper_client_output2.wav",
)
print(f"Audio 2 gespeichert unter: {output_path}")
