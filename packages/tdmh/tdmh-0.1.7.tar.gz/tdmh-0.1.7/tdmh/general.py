
import re
import os
import nltk
import math
from nltk import word_tokenize , sent_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
import string

from nltk.corpus import stopwords
stopwords = stopwords.words('english')

def tokenise( text ):
    tokens = []
    text = text.lower()
    text = re.sub( r'--' , ' -- ' , text)
    text = re.sub( r'-\"' , ' -- ' , text)
    text = re.sub( r'-\'' , ' -- ' , text)
    words = re.split( r'\s+' , text )
    for w in words:
        w = w.strip( string.punctuation )
        if re.search( r"[a-zA-Z]" , w ):
            tokens.append(w)
    return tokens

def flesch_kincaid( asl , asw ):
    fk = 0.39 * ( asl )
    fk = fk + 11.8 * ( asw )
    fk = fk - 15.59
    return fk


def sortedByValue( dict , ascending = True ):
    if ascending:
        return {k: v for k, v in sorted(dict.items(), key=lambda item: item[1])}
    else:
        return {k: v for k, v in reversed( sorted(dict.items(), key=lambda item: item[1]))}


def divideIntoSegments( full_text , nr_segments ):

    segments = []


    all_words = word_tokenise( full_text )

    segmentSize = int( len(all_words) / nr_segments )

    count_words = 0
    text = ''

    for word in all_words:
        count_words += 1
        text += word + ' '

        ## This line below used the modulo operator:
        ## We can use it to test if the first number is
        ## divisible by the second number
        if count_words % segmentSize == 0:
            segments.append(text.strip())
            text = ''
    return segments


def remove_extension(text):
    new_text = re.sub( '\.txt' , '' , text )
    return new_text

def removeStopWords( freq ):

    from nltk.corpus import stopwords
    stopwords_list = stopwords.words('english')

    filtered = dict()

    for w in freq:
            if w not in stopwords_list:
                filtered[w] = freq[w]

    return filtered

def countSyllables( word ):
    pattern = "e?[aiou]+e*|e(?!d$|ly).|[td]ed|le$|ble$|a$|y$"
    syllables = re.findall( pattern , word )
    return len(syllables)

def ptb_to_wordnet(PTT):

    if PTT.startswith('J'):
        ## Adjective
        return 'a'
    elif PTT.startswith('V'):
        ## Verb
        return 'v'
    elif PTT.startswith('N'):
        ## Noune
        return 'n'
    elif PTT.startswith('R'):
        ## Adverb
        return 'r'
    else:
        return ''


def remove_punctuation(words):
    new_list= []
    for w in words:
        if w.isalnum():
            new_list.append( w )
    return new_list


def remove_pg_boilerplate(complete_file):

    lines = re.split( r'\n' , complete_file )
    read_mode = 0
    full_text = ''

    for line in lines:
        #print(line)
        if read_mode == 1:
            full_text += line + '\n'

        if re.search( r'\*{3,}\s+START\s+OF\s+TH(E|IS)\s+PROJECT\s+GUTENBERG\s+EBOOK' ,  str(line) , re.IGNORECASE ):
            read_mode = 1
        if re.search( r'\*{3,}\s+END\s+OF\s+TH(E|IS)\s+PROJECT\s+GUTENBERG\s+EBOOK' ,  str(line) , re.IGNORECASE ):
            read_mode = 0

    full_text = full_text.strip()
    if re.search( r'^Produced by' , full_text , re.IGNORECASE ):
        full_text = full_text[ full_text.index('\n') : len(full_text) ]
    return full_text



def concordance_word( text, regex , width = 10 ):

    concordance = []
    distance = math.floor( width /2 )

    segment_length = 0

    words = word_tokenize( text )
    words = remove_punctuation( words )
    i = 0
    for w in words:
        if re.search( regex , w , re.IGNORECASE ):
            match = ''
            for x in range( i - distance , ( i + distance ) + 1 ):
                if x >= 0 and x < len(words):
                    if len(words[x]) >= 0:
                        match += words[x] + ' '
            concordance.append( match )

        i += 1

    return concordance


def collocation( text , regex , width ):

    freq_c = dict()
    distance = math.floor(width/2)

    sentences = sent_tokenize( text )

    for sentence in sentences:

        words = word_tokenize( sentence )
        words = remove_punctuation(words)

        for i,w in enumerate(words):
            if re.search( regex , w , re.IGNORECASE ):
                index_regex = i

                for x in range( i - distance , i + distance ):
                    if x >= 0 and x < len(words) and x != index_regex:
                        if len(words[x]) > 0:
                            word = words[x].lower()
                            freq_c[ word ] = freq_c.get( word , 0 ) + 1

    return freq_c


def remove_extension(text):
    new_text = re.sub( '\.txt' , '' , text )
    return new_text

def cooccurrence( text , word1 , word2 , width ):

    relevant_sentences = []

    text = re.sub( '\s+' , ' ' , text )
    sentences = sent_tokenize( text )

    for s in sentences:
        if re.search( r'\b' + word1 + r'\b' , s , re.IGNORECASE ) and re.search( r'\b' + word2 + r'\b' , s , re.IGNORECASE ):

            words = word_tokenize(s)
            word1_indexes = []
            word2_indexes = []

            for i,w in enumerate(words):
                if re.search( r'\b' + word1 + r'\b' , w , re.IGNORECASE ):
                    word1_indexes.append(i)
                elif re.search( r'\b' + word2 + r'\b' , w , re.IGNORECASE ):
                    word2_indexes.append(i)

            if word1_indexes[0] > word2_indexes[0]:
                difference = word1_indexes[0] - word2_indexes[0]
            else:
                difference = word2_indexes[0] - word1_indexes[0]

            if difference <= width:
                relevant_sentences.append(s)
    return relevant_sentences

lemmatiser = WordNetLemmatizer()
def lemmatise(full_text):
    sentences = sent_tokenize(full_text)
    lemmatised_text = ''

    for sent in sentences:
        words = word_tokenize(sent)
        words = remove_punctuation(words)
        pos = nltk.pos_tag(words)
        lemmatised_sent = ''

        for i,word in enumerate(words):
            word = word.lower()
            posTag = ptb_to_wordnet( pos[i][1] )

            if re.search( r'\w+' , posTag , re.IGNORECASE ):
                lemma = lemmatiser.lemmatize( words[i] , posTag )
                lemmatised_sent += lemma + ' '
            else:
                lemmatised_sent += word + ' '
        lemmatised_text += lemmatised_sent

    return lemmatised_text



def tokenise_remove_stopwords(full_text):
    words = word_tokenize(full_text)
    new_list= []
    for w in words:
        w = w.lower().strip()
        orig = ''
        if w.isalnum() and w not in stopwords:
            new_list.append( w )
    return new_list
