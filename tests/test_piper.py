from src.tts.piper_client import PiperClient

client = PiperClient(model_path="models/piper/de_DE-ramona-low.onnx")
output_path = client.generate(text="Hallo, ich bin Agent Birke.",output_filename="test_piper_client_output.wav",)
print(f"Audio 1 gespeichert unter: {output_path}")
output_path = client.generate(
    text="""
Wortherkunft
Das Wort Birke (von althochdeutsch bircha) ist auf einen Begriff im Indogermanischen zurückzuführen (bherHg̑o) und bedeutet in Anspielung auf die helle Rinde so viel wie „glänzend, schimmernd“ 
(vgl. noch mittelhochdeutsch bereht, englisch bright, -brecht (als Namensbestandteil) „leuchtend“).


Birken-Arten sind laubabwerfende, sommergrüne Bäume oder Sträucher. Sie gehören zu den sehr schnell und hochwachsenden Gehölzen und können schon nach sechs Jahren Wuchshöhen von bis zu 7 Metern erreichen; 
ausgewachsen können sie bis zu 30 Meter, in Einzelfällen sogar noch höher werden. Sie wachsen mit einzelnen oder oft auch mit mehreren Stämmen. Einzelexemplare können ein Alter von bis zu 160 Jahren erreichen.

Bei vielen Birken-Arten ist die Borke besonders auffällig, ihre Farbe reicht von fast Schwarz über Dunkel- und Hellbraun bis Weiß; sie ist anfangs glatt, später lösen sich dünne, oft papierartige Stücke ab, 
schließlich reißt sie horizontal auf. Es sind oft deutliche, meist dunkle Lentizellen vorhanden, die sich manchmal horizontal vergrößern.

Das leichte und je nach Art weiche bis mehr oder weniger harte Holz ist fast weiß bis rötlich-braun mit feiner Maserung. Bei jungen Zweigen können Lang- und Kurztriebe unterschieden werden. 
Die Zweige duften manchmal. Bei den Winterknospen überlappen sich mehrere glatte Schuppen.

Die wechselständig, meist zweireihig, oft an Kurztrieben angeordneten Laubblätter sind in Blattstiel und -spreite gegliedert. Die je nach Art mit Längen von 0,5 bis 10 (selten bis 14) Zentimetern und 
Breiten von 0,5 bis 8 Zentimetern eiförmigen bis deltaförmigen, elliptischen oder fast kreisförmigen Blattspreiten sind kahl bis unterschiedlich behaart, manchmal harzig-drüsig. Es liegt Fiedernervatur vor. 
Die Blattränder sind je nach Art gesägt bis meist doppelt gesägt oder seltener bei den nordischen Zwergstrauch-Arten gewellt bis leicht rundlich gelappt. Die Nebenblätter fallen oft früh ab.
    """,
    output_filename="test_piper_client_output2.wav",
)
print(f"Audio 2 gespeichert unter: {output_path}")
