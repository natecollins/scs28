#!/usr/bin/env python
# coding: utf-8
###############################################################################
# Copyright (c) 2015 Nathan Collins
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###############################################################################
"""
Super Card Shuffle 28!
~~~~~~~~~~~~~~~~~~~~~~

Can encode byte based strings into a common deck of cards, and then decode the
string back from the deck of cards.

Can also encrypt string messages into multiple decks of cards using Shamir's
Secret Sharing, and then decrypt the message from the decks of cards.

Encoding:
    ./scs28.py -e "Hello there."

Decoding, will prompt for card input:
    ./scs28.py -d

Decoding:
    ./scs28.py -d "6H 7C 10D 4C QD QC 7D 9C AH KC 3D 8C 3C 8H 2D 4H JC AC 6D KH 10H 9D 4D JH 2C AD 8D KD 9H 6C KS AS 3H 5C 7H 5D 10C 2S JD 2H QH 3S 4S 5S 6S 7S 8S 9S 10S JS QS 5H"

Encrypting, 3 shares with a threshold of 2 needed to decrypt:
    ./scs28.py --encrypt -n 3 -t 2 "Ssshh! Don't tell anyone."

Decrypting, will prompt for 2 deck inputs:
    ./scs28.py --decrypt -t 2
"""

from __future__ import print_function
import argparse
import sys
import math
import random
import codecs

__author__ = "Nathan Collins"
__copyight__ = "Copyright (c) 2015, Nathan Collins"
__licence__ = "MIT"
__version__ = "0.9.2"
__email__ = "npcollins<a>gmail_com"


###############################
## SCS28 Start 
###############################
def main(argv=None):
    apar = argparse.ArgumentParser(prog='scs28',
    description="""    Super Card Shuffle 28 -- 
    Converts a byte string message into a ordered deck of cards.
    Can also encrypt strings into multiple decks of cards using Shamir's Secret Sharing (SSS).
    """)
    apar.add_argument('message', metavar='MESSAGE', nargs='?',
            help='the message to encode/encrypt/decode/decrypt; if not given, will prompt')
    apar.add_argument('-e','--encode', action='store_true',
            help='encode simple message into a deck of cards; 28 characters maximum')
    apar.add_argument('-d','--decode', action='store_true',
            help='decode of simple message from a deck of cards; will prompt for card entry')
    apar.add_argument('-E','--encrypt', action='store_true',
            help='encrypt the message using SSS; 27 chars maximum; requires flags -t and -n')
    apar.add_argument('-D','--decrypt', action='store_true',
            help='decrypt using SSS; requires flag -t')
    apar.add_argument('-t', type=int, metavar='THRESH',
            help='sets the threshold for SSS; this is exact number of decks required to decrypt a message; can range from 2 to the total number of shares')
    apar.add_argument('-n', type=int, metavar='SHARES',
            help='sets the total share count for SSS; this is number of decks generated when encrypting a message; must be at least as large as the threshold; maximum value of 64')
    apar.add_argument('-v','--vertical', action='store_true',
            help='output decks in vertical columns instead of on single lines')
    apar.add_argument('-q','--quiet', action='store_true',
            help='do not print any prompts or help')
    apar.add_argument('--test', action='store_true',
            help=argparse.SUPPRESS)

    global pargs
    pargs = apar.parse_args(argv)

    # Choose action to perform
    if pargs.test:
        test()

    elif pargs.encode:
        ######################
        #### ENCODE CARDS ####
        ######################
        msg = b('')
        if pargs.message:
            msg = b(pargs.message)
        else:
            qprint ("Enter your message to encode:")
            qprint ("|------ 28 chars max ------|")
            msg = breadline()

        if len(msg) > 28:
            msg = msg[:28]
            print ("NOTICE: Message too long; truncating to:", msg, file=sys.stderr)

        mnum = messageToNumber(msg)
        encodedNums = encodeNumberToCards(mnum)

        deck = []
        for en in encodedNums:
            deck.append(en)
        decks = [ deck ]

        if pargs.vertical:
            outputDecksVertical(decks)
        else:
            for d in decks:
                outputDeckHorizontal(d)

    elif pargs.decode:
        ######################
        #### DECODE CARDS ####
        ######################
        if pargs.message:
            card_strs = pargs.message.split()
            deck = []
            for cstr in card_strs:
                cnum = cardToNumber(cstr)
                if cnum is None:
                    print ("FAILURE: Could not parse", cstr, "as a card. Use characters: C D H S A 1-10 T J Q K", file=sys.stderr)
                elif cnum in deck:
                    print ("FAILURE: Duplicate card", numberToCard(cnum), "detected. Please check your input.", file=sys.stderr)
                else:
                    deck.append(cnum)

            if len(deck) != 52:
                print("FAILURE: Given card list requires 52 cards, but", len(deck), "were provided.", file=sys.stderr)
                sys.exit(1)
        else:
            deck = deckInput()

        if len(deck) == 52:
            xnum = decodeCardsToNumber(deck)
            if pargs.quiet:
                print (numberToMessage(xnum))
            else:
                print ("\nDecoded:", numberToMessage(xnum))

    elif pargs.encrypt:
        #######################
        #### ENCRYPT CARDS ####
        #######################
        msg = b('')
        if not pargs.t or pargs.t < 2:
            print ("FAILURE: The threshold is not set properly (-t flag). If must be at least 2 and no more than the number of shares (the -n flag).", file=sys.stderr)
            sys.exit(1)
        if not pargs.n or pargs.t > pargs.n:
            print ("FAILURE: The number of shares is not set properly (-n flag). If must be at least as large as the threshold (the -t flag) and no larger than 64.", file=sys.stderr)
            sys.exit(1)

        if pargs.message:
            msg = b(pargs.message)
        else:
            qprint ("Enter your message to encrypt:")
            qprint ("|------ 27 chars max -----|")
            msg = breadline()

        secrets = messageToSecrets(msg, int(pargs.t), int(pargs.n))

        decks = []
        for sec in secrets:
            decks.append( secretToCards(sec) )

        if pargs.vertical:
            outputDecksVertical(decks)
        else:
            for d in decks:
                outputDeckHorizontal(d)

    elif pargs.decrypt:
        #######################
        #### DECRYPT CARDS ####
        #######################
        if not pargs.t or pargs.t < 2 or pargs.t > 64:
            print ("FAILURE: The threshold is not set properly (-t flag). If must match the threshold that was set when the decks were encrypted; can range from 2 to 64.", file=sys.stderr)
            sys.exit(1)

        secrets = []
        for di in range(0,pargs.t):
            secrets.append( cardsToSecret(deckInput()) )

        msg = secretsToMessage(secrets)
        if pargs.quiet:
            print (msg)
        else:
            print ("\nDecrypted:", msg)

    else:
        apar.print_help()

def breadline():
    """
    Having nothing to do with bread or rationing, this function grabs a
    binary line of data from input and returns it, for both Python 2 and 3
    """
    pyVer = sys.version_info
    if pyVer[0] == 2:
        return sys.stdin.readline().strip()
    return sys.stdin.buffer.readline().strip()

def b(s):
    """
    Shorthand function to convert str to bytes if running Python 3
    """
    pyVer = sys.version_info
    if pyVer[0] == 2:
        return s
    return str.encode(s)

def qprint(*args, **kwargs):
    """
    Print function, unless quiet flag was set
    """
    if not pargs.quiet:
        print(*args, **kwargs)


###############################
## Input and Output
###############################

def deckInput():
    """
    Loop user input into to grab a whole deck of cards. Provides prompts, already entered
    cards summary, options for canceling, and re-entering the previous card.
    User can choose the option to exit the program from within this loop.

    Returns:
        list: Always contains numbers 0 through 51 inclusive, ordered based on user input
    """
    cards = []
    instr = 'NONE'
    failcount = 0
    qprint ("Input your deck of cards below.")
    while len(cards) != 52 and instr:
        if instr == 'QUIT':
            sys.exit(0)

        cnums = []
        if instr == 'BACK':
            cards = cards[:-1]
        elif instr == 'REVIEW':
            outputDeckHorizontal(cards, "Deck so far: ")
        elif instr != 'NONE':
            clist = instr.split()
            for cl in clist:
                cnums.append(cardToNumber(cl))

        for cnum in cnums:
            if cnum is not None:
                failcount = 0
                if cnum in cards:
                    print ("FAILURE: Card", numberToCard(cnum), "is already in deck. Type 'review' to check.", file=sys.stderr)
                else:
                    cards.append(cnum)
            else:
                # to prevent piping in bad input from making a loop, quit if have too many failures
                failcount = failcount + 1
                if failcount > 12:
                    print("FAILURE: Too many failures during card entry. Quitting.", file=sys.stderr)
                    sys.exit(1)

        if len(cards) < 52:
            qprint("Cards entered:" ,len(cards), (" " if len(cards) == 0 else " Last card: " + numberToCard(cards[-1])))
            qprint("Enter card(s) [C D H S A 1-10 T J Q K] (review, back, quit): ", end='')
            instr = sys.stdin.readline().upper().strip()

    if not instr:
        print ("")

    if len(cards) != 52:
        print ("FAILURE: Did not receive a full deck as input where one was expected.", file=sys.stderr)
        sys.exit(1)

    return cards


def outputDecksVertical(decks):
    """
    Prints tab delimited vertical columns of card identifiers to stdout.

    Args:
        decks (list): A list containing decks; where a deck is a list of 52 unique numbers (0 - 51)
    """
    # reorder decks for output
    odecks = []
    for di in range(0,len(decks)):
        for ci in range(0,len(decks[di])):
            if len(odecks) < (ci+1):
                odecks.append( [decks[di][ci]] )
            else:
                odecks[ci].append( decks[di][ci] )

    for cidx in odecks:
        for cnum in cidx:
            print(numberToCard(cnum)+"\t", end='')
        print("")


def outputDeckHorizontal(deck, prefix=''):
    """
    Prints a space delimited line of card identifier for the deck provided.

    Args:
        deck (list): A deck, which is a list of 52 unique numbers (0 - 51)
        prefix (string): A label to print at the start of the line before the first deck is output
    """
    print (prefix, end='')
    for num in deck:
        print (numberToCard(num)+" ", end='')
    print("")


###############################
## Shamir's Secret Sharing
###############################

# A prime number larger than max number of chars we will be encrypting (2 ^ 216 bits).
# Encrypter/decrypter must be using the same prime number.
PRIME = 105312291668557186697918027683670432318895095400549111254310977959

def decGCD(a, b):
    if b == 0:
        return [a, 1, 0]

    recur = decGCD(b, a % b)
    return [ recur[0], recur[2], recur[1] - recur[2] * (a//b) ]


def modInv(k):
    k = k % PRIME
    n = -1 if k < 0 else 1
    r = n * decGCD(PRIME, n*k)[2]
    return (PRIME + r) % PRIME


def sssJoin(shares):
    joined = 0
    den = 1
    for f in range(0, len(shares)):
        num = den
        for c in range(0, len(shares)):
            if f == c:
                continue
            pstart = shares[f][0]
            pnext = shares[c][0]
            num = (num * -pnext) % PRIME
            den = (den * (pstart - pnext)) % PRIME

        val = shares[f][1]
        joined = (PRIME + joined + (val * num * modInv(den))) % PRIME

    return joined


def sssSplit(num, thresh, total):
    r = random.SystemRandom()
    shares = []
    coef = [num]

    for x in range(1, thresh):
        coef.append( r.randint(0, PRIME-1) )

    for x in range(1, total+1):
        accum = coef[0]
        for exp in range(1, thresh):
            accum = (accum + (coef[exp] * ((x ** exp) % PRIME) % PRIME)) % PRIME

        shares.append( [x, accum] )

    return shares

###############################
## Shares and Secrets
###############################

def shareToSecret(share):
    phex = "{0:0{1}x}".format(share[1], 54)
    return "{0:02x}".format(share[0]) + phex


def secretToShare(secret):
    share = []
    share.append( int(secret[:2], 16) )
    share.append( int(secret[2:], 16) )
    return share


def secretToCards(secret):
    secret_num = int(secret, 16)

    encodedNums = encodeNumberToCards(secret_num)

    encodedCards = []
    for en in encodedNums:
        encodedCards.append(en)

    return encodedCards


def cardsToSecret(encodedCards):
    encodedNums = []
    for ec in encodedCards:
        encodedNums.append(ec)

    secret_num = decodeCardsToNumber(encodedNums)
    secret = hexSecret(secret_num)
    secret = secret.rjust(56,'0')

    return secret


def hexSecret(secret_num):
    """
    Secret num to hex differences between Python 2 and 3
    """
    pyVer = sys.version_info
    if pyVer[0] == 3:
        return hex(secret_num)[2:]
    else:
        return hex(secret_num)[2:-1]

###############################
## Converting Messages
###############################

def messageToSecrets(msg, thresh=2, total=3):
    if total > 64:
        print("FAILURE: Max of 64 decks for secrets. You entered "+str(total)+", which is too many.", file=sys.stderr)
        sys.exit(1)
    if len(msg) > 27:
        print("WARNING: Message length truncated "+str(len(msg)-27)+" chars off the end (27 chars max).", file=sys.stderr)

    msg = msg[:27]
    num = messageToNumber(msg)
    shares = sssSplit(num, thresh, total)

    secrets = []
    for s in shares:
        secrets.append( shareToSecret(s) )

    return secrets


def secretsToMessage(secrets):
    shares = []
    for s in secrets:
        shares.append( secretToShare(s) )

    num = sssJoin(shares)
    msg = numberToMessage(num)
    return msg


def messageToNumber(msg):
    msg = msg.rjust(27,b('\0'))
    hexnum = codecs.encode(msg, 'hex');
    return int(hexnum,16)


def numberToMessage(num):
    hexnum = b("{0:0{1}x}".format(num, 54))
    return codecs.decode(hexnum, 'hex').strip(b('\0'))


###############################
## Cards as Numbers
###############################

def compat_translate(s):
    """
    Compatability function to support Python 2 and 3.1 style tranlate functions
    """
    pyVer = sys.version_info
    if pyVer[0] == 3 and pyVer[1] >= 1:
        return s.translate(str.maketrans('','',".-_:'"))
    else:
        return s.translate(None,".-_:'")


def numberToCard(num):
    if num > 51 or num < 0:
        print("FAILURE: Invalid card number: "+str(num), file=sys.stderr)
        sys.exit(1)

    nsuit = num // 13
    suit = "C"
    if (nsuit == 1):
        suit = "D"
    elif (nsuit == 2):
        suit = "H"
    elif (nsuit == 3):
        suit = "S"

    card = str((num % 13) + 1)
    if (card == "1"):
        card = "A"
    elif (card == "11"):
        card = "J"
    elif (card == "12"):
        card = "Q"
    elif (card == "13"):
        card = "K"

    return card + suit


def cardToNumber(cstr):
    cstr = compat_translate( cstr.upper().strip() )
    suit = ""
    card = ""
    if (cstr[0] in "CDHS"):
        suit = cstr[0]
        card = cstr[1:]
    elif (cstr[-1] in "CDHS"):
        suit = cstr[-1]
        card = cstr[:-1]

    nsuit = 0;
    if (suit == "D"):
        nsuit = 1
    elif (suit == "H"):
        nsuit = 2
    elif (suit == "S"):
        nsuit = 3

    ncard = -1
    if (card == "A"):
        card = "1"
    elif (card == "T"):
        card = "10"
    elif (card == "J"):
        card = "11"
    elif (card == "Q"):
        card = "12"
    elif (card == "K"):
        card = "13"

    if (card.isdigit()):
        ncard = int(card) - 1
        if ncard < 0 or ncard > 12:
            ncard = -1

    num = None
    if ncard == -1 or suit == "":
        print("FAILURE: Invalid card "+cstr, file=sys.stdout)
    else:
        num = (nsuit * 13) + ncard

    return num


###############################
## Encoding Data into Decks
###############################

def swap(l, p1, p2):
    t = l[p1]
    l[p1] = l[p2]
    l[p2] = t
    return l


def swapLeft(l, v, n):
    for x in range(0,n):
        i1 = l.index(v)
        i2 = i1 - 1
        if i2 < 0:
            i2 = len(l) - 1;
        l = swap(l, i1, i2)
    return l


def swapRight(l, v, n):
    for x in range(0,n):
        i1 = l.index(v)
        i2 = i1 + 1
        if i2 >= len(l):
            i2 = 0;
        l = swap(l, i1, i2)
    return l


def encodeNumberToCards(number):
    cardList = range(0,52)
    # card values
    cv = []
    for i,c in reversed(list(enumerate(cardList))):
        cv.append( (c, math.factorial(i+1)) )

    # generate encoding instructions
    instr = []
    i = len(cv)
    cn = number
    for c,v in cv:
        instr.append( (c, cn // v) )
        cn = cn - (cn // v) * v
        i = i - 1
    instr.reverse()

    # encode number in cards
    ec = list(cardList)
    for cmd in instr:
        crd, cnt = cmd
        ec = swapLeft(ec, crd, cnt)

    return ec


def decodeCardsToNumber(encodedCards):
    cardList = range(0,52)
    # card values
    cv = []
    for i,c in reversed(list(enumerate(cardList))):
        cv.append( (c, math.factorial(i+1)) )
    cv.pop(0)

    # decode cards to extract number
    xnum = 0
    es = list(encodedCards)
    i = len(cv)
    for c,v in cv:
        i = i - 1
        while es[i] != c:
            es = swapRight(es, c, 1)
            xnum = xnum + v

    return xnum


###############################
## Check How Broken Things Are
###############################

def test():
    """
    Perform a quick test to make sure everything works.
    """
    message = b("Super Card Shuffle 28!")

    print("Encoding message: ", message)
    mnum = messageToNumber(message)
    deck = encodeNumberToCards(mnum)
    xnum = decodeCardsToNumber(deck)
    print("Decoded message:", numberToMessage(xnum))

    print("Encrypting message: ", message)
    secrets = messageToSecrets(message)

    # convert secrets to cards and print in orderly columns
    decks = []
    for sec in secrets:
        deck = secretToCards(sec)
        decks.append( deck )

    outputDecksVertical(decks)
    for d in decks:
        outputDeckHorizontal(d)

    # Pass secrets through card encoder/decoders
    for si in range(0,len(secrets)):
        ctransformed = cardsToSecret( secretToCards(secrets[si]) )
        print ("Cards in deck", si+1, "decoded ok:", (ctransformed == secrets[si]))

    print("\nTesting combine...")
    secrets.pop( random.randint(0, len(secrets)-1) )
    message = secretsToMessage(secrets)
    print("Decrypted message: ", message)


###############################
if __name__ == "__main__":
    sys.exit(main())


