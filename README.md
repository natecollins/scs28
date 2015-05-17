Super Card Shuffle 28!
=============================

Super Card Shuffle 28! (SCS28) can encode or encrypt messages into standard full decks of 52 cards for covert transport.  

Written in Python and tested on Linux/OS X/Windows.  


1. [Why Use Card Decks?](#why-use-card-decks)
2. [Example Situation](#example-situation)
3. [Disclaimer](#disclaimer)
4. [Suggestions for Use](#suggestions-for-use)
5. [Encoding/Decoding](#encoding-decoding)
6. [Encrypting/Decrypting](#encrypting-decrypting)
7. [Copyright](#copyright)


Why Use Card Decks?
-----------------------------
Encoding data into a deck of cards was something I did for fun. Combining cards as a data store along with Shamir's Secret Sharing (SSS) to provide some actual cryptographical use is just icing on the cake.  

In terms of transport, a deck of cards is something inconspicuous enough to actually be carried by an average person while travelling without drawing unwanted attention. With the addition of SSS, this allows for distributed transport of a message with some security and redundancy.  


Example Situation
-----------------------------
Here's an example transport situation: __Adam__ want to transport a secret key securely to __Bill__, but __Eve__ is trying to intercept all messages. __Bill__ does not believe there is any secure way to do this electronically without attracting unwanted attention from __Eve__. To get by __Eve__, __Adam__ decides to encoded the key in 5 decks of cards with a threshold of 3 decks, meaning at least 3 deck are needed to recreate the key.  

__Adam__ entrusts 5 different couriers each with 1 deck, and sends them to __Bill__ by a different route. Each individual courier's deck is completely worthless on its own and will not reveal any data if intercepted by __Eve__. Further, if __Eve__ is able to detain a courier and inspect/shuffle the deck of a second courier, the key message can still be received so long as at least 3 untainted decks make it to __Bill__. And even _if_ 3 or more decks are intercepted, it would be highly unlikely that the interceptors would realize that different decks of cards on different routes could be a means of communication, and combine them to re-create the secret key.  


Disclaimer
-----------------------------
I provide no guarantee of any kind with regards to this script. If you use SCS28 as a means of sending secrets and then it turns out the script has a bug which results in your embarrassment or shame, you're on your own. Don't come crying to me.  

The code is pretty simple, so check it out yourself and make sure you know what your entrusting your secrets to before using it for serious purposes. Actually, for serious cryptography you should probably go elsewhere; I just did this for the fun of it.  


Suggestions for Use
-----------------------------
The order of cards in the deck is important, in fact, that's pretty much of all that matters. So if you use a Joker card to indicate the start of the deck ordering _AND_ learn a good false shuffle, you should be able to "play" with your deck (i.e. fake shuffling while you wait) to belay suspicion that the deck contains data.  

If sending decks on different routes or at different times, via multiple couriers, make sure to use different types of decks or different quality. If __Eve__ notices that a whole host of individuals keep passing by with crisp new black label Tricycle brand cards, she might get suspicious.  

I've provided hash files to verify the script file against, but if you think the download of the script was compromised, you should expect the download of the hashes could be compromised as well. So if you're paranoid, don't trust your downloads and re-read the disclaimer above.    


Encoding/Decoding
-----------------------------

The simplest means of using SCS28 is to simply store a message into a deck of cards. This is not encrypted in any way, so anyone who decides to decode the deck will be able to read the message with just the single deck. Max of 28 characters allowed per deck.  

Encode Examples:
```
./scs28.py -e "Hey, I'm in a deck of cards!"
AH KH 8S JS 9D AD 10D 5D 2S JH 6C 10H 2H 7H AC 10S 5C 3S 7D 8C 4D QD KC AS 8D 6D 4C 3H 10C 8H 6S 2D 4H 9H 3D JC JD 7C 2C QH KD 3C 6H 7S 4S 9C QS 5S KS 9S QC 5H
```

Will prompt for input if not given on the command line.
```
./scs28.py -e
Enter your message to encode:
|------ 28 chars max ------|
Van Gelder wants asylum.
JD 7C KD 9D 2D 10D 8D 3C 8C JC 4C 3D 4D 10C 6D 2C KC 5C 9C 5D QD QC 6C AC AD AH KS 2H 3H 4H 5H 6H 7H 8H 9H 10H JH QH KH AS 2S 3S 4S 5S 6S 7S 8S 9S 10S JS QS 7D
```

Decode Examples:
```
./scs28.py -d "JD 6C 3C 4D 3D 10D QD 2D KS AH KC 7C 10C 5D 8C 8D 5H 3H QC AD 2H 4H 7D 9C 6D 5C JC AC 9D 4C 6H KD 7H 8H 9H 10H JH QH KH AS 2S 3S 4S 5S 6S 7S 8S 9S 10S JS QS 2C"
Decoded: I FEEL FINE
```

Again, will prompt for input if nothing to decode is provided.
```
./scs28.py -d
Input your deck of cards below.
Cards entered: 0  
Enter card(s) [C D H S A 1-10 T J Q K] (review, back, quit): 5s
Cards entered: 1  Last card: 5S
Enter card(s) [C D H S A 1-10 T J Q K] (review, back, quit): th
Cards entered: 2  Last card: 10H
Enter card(s) [C D H S A 1-10 T J Q K] (review, back, quit): qc
Cards entered: 3  Last card: QC
Enter card(s) [C D H S A 1-10 T J Q K] (review, back, quit): jd kh 5h 1h 10c 9D
Cards entered: 9  Last card: 9D
Enter card(s) [C D H S A 1-10 T J Q K] (review, back, quit): h6 ad 9C 8H 4d
Cards entered: 14  Last card: 4D
Enter card(s) [C D H S A 1-10 T J Q K] (review, back, quit): 4s Kc 5g qh 7h
Cards entered: 19  Last card: 7H
Enter card(s) [C D H S A 1-10 T J Q K] (review, back, quit): kd 3d 2h 3s d7 c5 6s 4c
Cards entered: 27  Last card: 4C
Enter card(s) [C D H S A 1-10 T J Q K] (review, back, quit): jc jh 2c sa d10 dq 8d
Cards entered: 34  Last card: 8D
Enter card(s) [C D H S A 1-10 T J Q K] (review, back, quit): AC 3c 8c 2s h4 ks 2d 7c
Cards entered: 42  Last card: 7C
Enter card(s) [C D H S A 1-10 T J Q K] (review, back, quit): d6 6c h9 7s 8S 9s
Cards entered: 48  Last card: 9S
Enter card(s) [C D H S A 1-10 T J Q K] (review, back, quit): s10 js qs
Cards entered: 51  Last card: QS
Enter card(s) [C D H S A 1-10 T J Q K] (review, back, quit): 3h
Decoded: professionals target people
```

Encrypting/Decrypting
-----------------------------

You can encrypt a message into multiple decks using Shamir's Secret Sharing with the `--encrypt` flag. Also needed is a threshold flag `-t` and a total number of shares flag `-n`. The number of shares is how many separate decks will be created, and the threshold is how many of those decks are needed to re-create the original message. Max of 27 characters allowed in encrypted messages.  

Encrypting Examples:
```
./scs28.py --encrypt -t 2 -n 3 "Talk is cheap"
3D 8C KC 10C 5S 4H 2C 8D 5H 10D 9H 6S 3S 3H AS 10S 9S 6D KS 4C KD 6C 5C AD 2D 9D 4S JH QC QD QH 6H AH 7D 10H 5D 7H 8H JD AC JC 9C 7S 2H 2S KH JS 8S 3C 7C QS 4D 
JC 4S AD 7H 9C JH 4H AC 8C QC 5S QH 7C 8D 6C 2C QD 2H 10H KS 10D KD 5H 6S 10C 3S 5D 9H AS 8H 3D 10S 6D 9S AH KC 7S JD 4C 9D 2S 3H JS 5C KH 8S 2D 3C 4D 7D QS 6H 
9S QC 4H KS 10H QD 2D 10C 8C 7D 2C 3H 6H 3D 7H 8H 5S 8D KC 9C JC 5D KD 7C AH JD 4S 10D AC 7S JH AD 5H 2S 3C 4C KH 6S JS 5C 3S 2H 8S QH 9H 9D AS 6C 4D 10S QS 6D
```

Can also print the decks veritcally for easier reading:
```
./scs28.py --encrypt -v -t 3 -n 5
Enter your message to encrypt:
|------ 27 chars max -----|
To hold a pen
5H  4D  JD  10S KC  
3D  2C  4C  10D 2H  
8D  AC  2D  KD  AH  
8H  10H 7S  7C  5D  
JD  5C  3S  9C  9C  
10H 7H  4D  6S  10D 
QC  JC  2C  5C  6C  
6C  9D  10D JH  5S  
QH  10C 9H  AH  QH  
6D  KD  JC  3D  QC  
9D  9C  3H  4S  2C  
10C 10D 3C  9S  4H  
2D  3S  AH  JC  5C  
QD  7C  6C  2C  9S  
KC  6S  4H  AD  JH  
3S  AS  AS  5D  KS  
5S  AD  5S  10H 6S  
3H  6H  10H 2S  KD  
4D  6D  7C  8D  QD  
5D  QD  5D  7S  10C 
7H  3C  KH  10C 10S 
KS  7D  QD  3S  9D  
4S  6C  9C  2H  3D  
AC  5D  9D  8H  JD  
KH  5H  10S 3H  8S  
2C  QC  5H  2D  4D  
7D  9S  10C QD  2D  
9C  8H  AD  8S  5H  
JH  9H  9S  KS  4S  
2H  AH  8D  JD  KH  
4H  KS  AC  AC  JS  
7C  8S  4S  7D  3S  
2S  KH  7D  4D  3C  
8S  4S  KD  4H  AD  
6S  4C  5C  9H  10H 
10D 2H  JH  JS  6D  
KD  3H  JS  KH  7D  
3C  2D  QH  AS  AS  
8C  2S  3D  6C  8H  
9H  10S 6D  6D  4C  
4C  JH  KC  QC  7C  
7S  JS  6S  6H  7S  
AD  KC  QC  KC  6H  
JS  JD  8H  7H  2S  
JC  8C  6H  5H  3H  
6H  4H  2H  9D  8C  
9S  7S  2S  5S  AC  
AS  3D  7H  4C  9H  
5C  8D  8C  3C  8D  
10S QH  KS  QH  7H  
QS  QS  QS  QS  QS  
AH  5S  8S  8C  JC
```

Decrypting Examples:

You may enter multiple cards, up to a full deck, at the input prompts.
```
./scs28.py --decrypt -t 2
Input your deck of cards below.
Cards entered: 0  
Enter card(s) [C D H S A 1-10 T J Q K] (review, back, quit): 5D 8H 8C 10H 6H KC AD QD 3D 2D 2C 10D 3H KH 2H AH 6D KS 5S JH 2S 3S 9D 7D 4D 8S JD 3C QH 7C 4C 10C 5C 8D 6C 5H KD 9S 9C 4H JS 7S 9H QC AS 4S AC 6S JC 7H QS 10S
Input your deck of cards below.
Cards entered: 0  
Enter card(s) [C D H S A 1-10 T J Q K] (review, back, quit): AS QH 6C 9D 9H 2H 7S 5S 3S JH 8C 3C 10D AD 5H 6D 5C JC 7D 8H 6H AH 8S 10S 10H 10C KC JD QC 2D 4C 2C 9S JS 7C QD 4D KH 2S AC KD 3D 4S 6S 9C 4H 5D KS 8D 7H QS 3H
Decrypted: Two plus two make four.
```

Copyright
-----------------------------

This is released under the MIT open source license. See the LICENCE file for details.



