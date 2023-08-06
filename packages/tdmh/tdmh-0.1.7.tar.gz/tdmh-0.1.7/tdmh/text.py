
import re
import math
import os
from os.path import isfile, join , isdir
import string

import nltk
from nltk.stem import WordNetLemmatizer




class text:

    full_text = ''
    file_name = ''
    tokens = 0
    types = 0

    def __init__(self, file_name ):
        self.file_name = file_name
        self.segments = []

        tokens_count = 0
        if re.search( r'\.txt$' , self.file_name ):
            try:
                freq = dict()
                freq.clear()
                text = open( self.file_name , encoding = 'utf-8' , errors = 'ignore' )
                for s in text:
                    self.segments.append(s)
                    words = word_tokenise(s)
                    for w in words:
                        tokens_count += 1
                        freq[w] = freq.get(w,0) + 1
            except:
                print( "Cannot read " + self.file_name + " !" )

            self.types = len(freq)
            self.tokens = tokens_count

    def __str__(self):
        return f'The text contains the contents of { self.file_name }'

    def title( self ):
        title = os.path.basename( self.file_name )
        title = re.sub( r'[.]txt$' , '' , title )
        return title

    def tokens( self ):
        return self.tokens

    def concordance( self , searchTerm , distance ):

        concordance = []
        regex = r'\b{}\b'.format( searchTerm )

        segment_length = 0

        for line in self.segments:
            line = line.strip()
            words = word_tokenise( line )
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

    def concordance_char( self , search_term,window ):

        concordance = []

        regex = r'\b{}\b'.format( search_term )

        for line in self.segments:
            line = line.strip()

            if re.search( regex , line , re.IGNORECASE ):
                extract = ''
                position = re.search( regex , line , re.IGNORECASE ).start()
                start = position - len( search_term ) - window ;
                fragmentLength = start + 2 * window  + 2 * len( search_term )
                if fragmentLength > len( line ):
                    fragmentLength = len( line )

                if start < 0:

                    whiteSpace = ''
                    i = 0
                    while i < abs(start):
                        whiteSpace += ' '
                        i += 1
                    extract = whiteSpace + line[ 0 : fragmentLength ]
                else:
                    extract = line[ start : fragmentLength ]

                if re.search( '\w' , extract ) and re.search( regex , extract , re.IGNORECASE ):
                    concordance.append( extract )

        return concordance


    def collocation( self , searchTerm , distance ):

        regex = r"\b" + searchTerm.lower() + r"\b"
        freq_c = dict()

        words = []

        paragraph = ''
        parLength = 0


        for line in self.segments:
            line = line.strip()
            if parLength < 100:
                parLength += len(line)
                paragraph += line + ' '
            else:
                parLength = 0
                words = word_tokenise( paragraph )
                i = 0
                for w in words:
                    if re.search( regex , w , re.IGNORECASE ):

                        for x in range( i - distance , i + distance ):
                            if x >= 0 and x < len(words) and searchTerm != words[x]:
                                if len(words[x]) > 0:
                                    freq_c[ words[x] ] = freq_c.get( words[x] , 0 ) + 1


                    i += 1
                paragraph = ''
        return freq_c



    def calculate_word_frequencies( self ):
        freq = dict()
        for line in self.segments:
            words = word_tokenise( line  )
            for w in words:
                freq[w] = freq.get( w , 0) + 1
        return freq



    def lemmatise( self ):
        lemmatised_text = ''
        lemmatiser = WordNetLemmatizer()
        for line in self.segments:
            words = word_tokenise(line)
            pos = nltk.pos_tag(words)

            for i in range( 0 , len(words) ):
                posTag = ptb_to_wordnet( pos[i][1] )
                if re.search( r'\w+' , posTag , re.IGNORECASE ):
                    lemma = lemmatiser.lemmatize( words[i] , posTag )
                else:
                    lemma = lemmatiser.lemmatize( words[i] )
                lemmatised_text += lemma + ' '
            lemmatised_text += '\n'
        return lemmatised_text

    def word_tokenise( text ):
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

    def sortedByValue( dict ):
        return sorted( dict , key=lambda x: dict[x])


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


    def removeExtension(text):
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
