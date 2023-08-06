import cutters

text = """
DINAMO i Hajduk u nastavak prvenstva ušli su s po dvije pobjede, a dva najveća hrvatska kluba su prije toga odradila i više nego uspješan prijelazni rok. Dinamo je u momčadi ostavio Mislava Oršića te doveo Petra Bočkaja i Mehira Emrelija dok je Hajduk momčad osnažio Ferrom, Grgićem, Mikanovićem i najvećim pojačanjem Nikolom Kalinićem.

Hajduk je i dalje pet bodova iza Dinama te dva iza Osijeka i Rijeke, no Splićani izgledaju puno, puno jače nego što su bili ujesen. Slično razmišljaju i kladionice prema kojima je Dinamo i dalje veliki favorit za naslov. Na branitelja naslova koeficijent je 1.50, na Hajduk 4.50, na Osijek 6, a na Rijeku čak 10. Tko je favorit i tko je jači pitali smo nekoliko hrvatskih trenera.

"Dolascima svih ovih igrača u zimskom prijelaznom roku Hajduk je definitivno pokazao da će se boriti za naslov prvaka već ove sezone. To je sad jedna dobra, iskusna momčad koja je dovoljno jaka da nešto može osvojiti. No, reći da je Hajduk sad preko noći najednom favorit za naslov prvaka bilo bi neozbiljno", kaže bivši Dinamov igrač i trener Nikola Jurčević i nastavlja:

"Dinamo ima pet bodova prednosti i dugogodišnju naviku osvajanja titula. Doveo je Emrelija i Bočkaja koji su jako dobri igrači i Dinamo je za mene i dalje favorit broj jedan uz dužno poštovanje konkurentima. Što se Kalinića tiče, on unatoč godinama i dalje djeluje fit i siguran sam da dolazi s ogromnom motivacijom da pomogne Hajduku."

Marko Livaja ove sezone igra fantastično, a dolaskom Kalinića mogla bi nastati gužva u napadu. Riječ je o dva različita napadača, ali Jurčević smatra da će oni dobro surađivati i da će to biti veliki plus za Hajduk.

"Kalinić je klasični centarfor, a Livaja se više povlači u igru i ne vidim zašto ne bi dobro funkcionirali. Kalinić je unatoč godinama i dalje u odličnom stanju koji će pomoći iskustvom i kvalitetama. On se jako želio vratiti u Hajduk, tako je to s igračima od dolje. Njima je Hajduk sve, to je fenomen Splita i toga kluba i on je sigurno došao ostaviti trag", dodao je Jurčević.

Dinamo je doveo Emrelija, igrača kojeg je Jurčević vodio dok je bio izbornik azerbajdžanske reprezentacije. On je došao iako je Oršić ostao, a bivši Dinamov trener to vidi kao dobar i logičan potez zbog onoga što dolazi.

"Emreli je fizički jako moćan igrač. Nije klasična špica, nego igrač sličan Oršiću, ima dobru lijevu nogu i može igrati i polušpicu i na oba krila. U Dinamu uvijek razmišljaju dva koraka unaprijed i vjerojatno računaju da će na ljeto ostati bez Petkovića ili Oršića ili obojice. Emreli je potencijal, mlad je i Dinamo s njim nije puno riskirao, a može dosta dobiti", smatra Jurčević i dodaje:

"Dinamo je ipak drugi nivo u odnosu na klubove u kojima je dosad igrao, ali on ipak ima međunarodno iskustvo igranja u reprezentaciji te u Karabahu i Legiji s kojima je igrao Europu. Takva konkurencija bit će dobra i za ostale igrače i u Dinamu nemaju razloga za brigu."

"Hajduk je napravio sve potrebno da već ove sezone bude konkurentan. No, ako si stave pritisak da moraju odmah biti prvaci, to neće biti dobro. Ne smije biti kraj svijeta ako ne osvoje titulu, nego se okrenuti sljedećoj sezoni i pokušati napasti", zaključio je Jurčević.

"Jako puno će ovisiti o onoj zaostaloj utakmici. Hajduk to mora dobiti i nema mu druge. Ako u tome uspije, onda je sve otvoreno, ali ako bude neriješeno ili Dinamo pobijedi, teško će do naslova. Dovođenjem ovih igrača Hajduk je pokazao da misli ozbiljno. Po meni su bliže trofeju u Kupu koji, ako sad ne osvoje, ne znam kad će. Imaju doma dvije utakmice i veliku šansu", kaže Toplak i nastavlja:

"No Dinamo je također pokazao zube. Ostavio je Oršića i dovođenjem Bočkaja i Emrelija poslao dovoljno jaku poruku da se ne namjerava odreći naslova. Dinamo i dalje ima najširi kadar, strašno je jak, ima pet bodova prednosti što nije zanemarivo i za mene je i dalje favorit."

Toplak smatra da će zanimljivo biti vidjeti kako će Dambrauskas uklopiti Kalinića i Livaju u momčad. Hajdukov trener je protiv Gorice igrao u sustavu 3-5-2 u kojem, ako tako nastavi, sad više neće biti mjesta za mlade igrače.

"Hajduk sad igra jako dobro i nekad nije pametno previše talasati i mijenjati ono što funkcionira. Livaja jako dobro funkcionira kao devetka i ima slobodu u igri. Kalinić je klasični centarfor i što ćeš sad sa svojim najboljim igračem? Zašto njega izmišljati na nekoj drugoj poziciji? Svaki dobar igrač u kadru je plus, ali to može biti zamka jer remeti atmosferu", smatra Toplak i dodaje:

"Ono što mi sa strane ne znamo jest koliko je to sve skupa u Hajduku financijski održivo, ali vjerujem da znaju što rade. Kalinić s 34 godine sigurno nije adut u dugoročnom planu. On košta i to ti mora vratiti trofejem. S druge strane, sumnjam da su toliko riskirali i bacili sve karte na ovu sezonu. Napravili su dobar posao, s Ferrom i Grgićem dobili su dodatnu kvalitetu i mogu se nadati."
"""

text = """
    Petar Krešimir IV. je vladao od 1058. do 1074. St. Louis 9LX je događaj u svijetu šaha. To je prof.dr.sc Ivan Ivanić, pored njega je doc.sc. Marko Markić itd. Tolstoj je napisao: "Sve sretne obitelji nalik su jedna na drugu. Svaka nesretna obitelj nesretna je na svoj način."
"""

text = """
Petar Krešimir IV. je vladao od 1058. do 1074. St. Louis 9LX je događaj u svijetu šaha. To je prof.dr.sc. Ivan Horvat. Volim rock, punk, funk, pop itd. Tolstoj je napisao: "Sve sretne obitelji nalik su jedna na drugu. Svaka nesretna obitelj nesretna je na svoj način."
"""

sentences = cutters.cut(text, "hr")

# print(sentences[4].quotes[0].sentences[0])
print(sentences)

# for sentence in sentences:
# print(f"Sentence: {sentence.str}")
# for quote in sentence.quotes:
# print(f"Quote: {quote.str}")
# for quote_sentence in quote.sentences:
# print(f"Quote sentence: {quote_sentence}")
