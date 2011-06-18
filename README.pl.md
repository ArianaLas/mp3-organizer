MP3 Organizer
=============

Automatycznie organizuj, sortuj lub zminiaj nazwy plików Twojej kolekcji muzycznej.

Wymagania
=========

* Python 3
* stagger (http://code.google.com/p/stagger/)

W Arch Linux po prostu napisz:

	# pacman -Sy python
	$ yaourt -S python3-stagger-svn

Jeżeli nie korzystasz z Yaourta, pobierz *PKGBUILD* dla paczki *python3-stagger-svn* z AUR i ręcznie stwórz pakiet:
	
	$ makepkg

Następnie pakiet ten zainstaluj korzystająć z  *pacman -U*.

Instalacja
==========

Po prostu przenieś *mp3-organizer.py* do dowolnego katalogu z PATH np.:

	# mv mp3-organizer.py /usr/bin/mp3-organizer
	# chmod +x /usr/bin/mp3-organizer # (nadaj prawa uruchomienia)

Przykłady
=========

	$ mp3-organizer -p ~/Music/ -t ~/Music/ -r --recognize-covers

Rekurencyjnie (przeglądaj również katalogi w katalogach) organizuj katalog *~/Music/* (opcja -p), pliki wynikowe składuj w tym samym katalogu (opcja -t). Dodatkowo próbuj rozpoznawać okładki (opcja --recognize-covers).

	$ mkdir ~/Music # (tworzenie pustego katalogu ~/Music)
	$ mp3-organizer -v -p ~/ -t ~/Music/ -r -d

Znajdź wszystkie pliki MP3 w katalogu domowym i przenieś je do ~/Music, wypisuj dokładnie co robisz (opcja -v). Próbuj usuwać katalogi z których przeniesiono muzykę (tylko jeżeli są puste).

	$ mp3-organizer -v -c -p ~/Music/Iron\ Maiden/ -t /media/TELEFON/Muzyka --scheme {artist}-{album}/{track}-{title}

Skopiuj (opcja -c) wszystkie pliki MP3 z katalogu *~/Music/Iron Maiden/* do katalogu */media/TELEFON/Muzyka/*, jako schemat przyjmij *{artist}-{album}/{track}-{title}*

Przykładowy plik:

	~/Music/Iron Maiden/When-the-Wild-Wind-Blows.mp3

Zostanie skopiowany do:

	/media/TELEFON/Muzyka/*Iron Maiden-The Final Frontier/10-When the Wild Wind Blows.mp3*

Podrubiona część powstała w wyniku zstosowania schematu (opcja --scheme).

Domyślnym schematem programu jest:
	
	{artist}/{album}/{title}

License
=======

Copyright (C)
* Patryk Jaworski <skorpion9312@gmail.com>
* Ariana Las <ariana.las@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see http://www.gnu.org/licenses.

License - PL
============

Copyright (C)
* Patryk Jaworski <skorpion9312@gmail.com>
* Ariana Las <ariana.las@gmail.com>

Niniejszy program jest wolnym oprogramowaniem - możesz go rozpowszechniać dalej
i/lub modyfikować na warunkach Powszechnej Licencji Publicznej GNU wydanej przez
Fundację Wolnego Oprogramowania, według wersji 3 tej Licencji lub dowolnej
z późniejszych wersji.

Niniejszy program rozpowszechniany jest z nadzieją, iż będzie on użyteczny - jednak
BEZ ŻADNEJ GWARANCJI, nawet domyślnej gwarancji PRZYDATNOŚCI HANDLOWEJ
albo PRZYDATNOŚCI DO OKREŚLONYCH ZASTOSOWAŃ. Bliższe informacje na ten temat
można uzyskać z Powszechnej Licencji Publicznej GNU.

Kopia Powszechnej Licencji Publicznej GNU powinna zostać ci dostarczona razem
z tym programem. Jeżeli nie została dostarczona, odwiedź http://www.gnu.org/licenses.

Nieoficjalne, tłumaczenie licencji znajdziesz pod adresem: http://itlaw.computerworld.pl/index.php/gpl-3/
