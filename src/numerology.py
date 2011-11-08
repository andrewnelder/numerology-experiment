#encoding=UTF-8
'''
This is a study that is based on my idle curiosities regarding numerology.
According to the divination experts, numerology's most important calculation
relates to that of your birth.  By taking the dates of 

This study looked at (from what I understand of the field) the most common
method for deriving this value.  It also considers master numbers: 11 and 22.

Basic definitions of life path meanings were extracted from 
Astrology-Numerology (c) Michael McClain 1996-2011.
[http://www.astrology-numerology.com/]

Sample datasets were extracted from Freebase (c) Metaweb 2011.
[http://www.freebase.com/]

Created on Nov 7, 2011
@author: andrewnelder
'''

from collections import defaultdict
from csv import reader
from logging import getLogger, basicConfig, DEBUG

MASTER_NUMBERS = [11,22]

LIFEPATH_COUNT = defaultdict(int)
LIFEPATH_DEFS = {1: 'The Life Path 1 suggests that you entered this plane '
                    'with skills allowing you to become a leader type rather '
                    'easily.',
                 2: 'The Life Path 2 suggests that you entered this plane '
                    'with a spiritual quality in your makeup allowing you to '
                    'be one of the peacemakers in society.', 
                 3: 'The Life Path 3 indicates that you entered this plane '
                    'with a strong sense of creativity and with wonderful '
                    'communication skills.',
                 4: 'The Life Path 4 suggests that you entered this plane '
                    'with a natural genius for planning, fixing, building, '
                    'and somehow, with practical application and cerebral '
                    'excellence, making things work.',
                 5: 'The Life Path 5 suggests that you entered this plane '
                    'with a highly progressive mindset, with the attitude and '
                    'skills to make the world a better place.',
                 6: 'The Life Path 6 suggests that you entered this plane '
                    'with tools to become the ultimate nurturer, and a beacon '
                    'for truth, justice, righteousness, and domesticity.',
                 7: 'The Life Path 7 suggests that you entered this plane '
                    'with a gift for investigation, analysis, and keen '
                    'observation.',
                 8: 'The Life Path 8 suggests that you entered this plane '
                    'armed to lead, direct, organize and govern.',
                 9: 'The Life Path 9 suggests that you entered this plane '
                    'with an abundance of dramatic feelings coupled with a '
                    'strong sense of compassion and generosity.',
                 0: 'The Master Life Path suggests that you are destined for '
                    'greatness.'}

LOGGER = getLogger(__name__)

def date_to_number(birthdate):
    '''
    Convert a birth-date to a life-path number.
    
    @param birthdate:
        Birthdate to reduce.  Must be in form [YYYY-MM-DD].
    @type birthdate:
        str
    '''
    
    if len(birthdate) != 10:
        raise ValueError('Birthdate must be in the form YYYY-MM-DD ' \
                         + '(1985-10-15).')
    
    # acquire d-m-y
    (year, month, day) = birthdate.split('-')
    
    # convert to int
    year = int(year)
    month = int(month)
    day = int(day)
    
    # perform reduction on day and year
    day = sum_chars(day)
    year = sum_chars(year)
    
    return sum_chars(day+month+year)

def log_result(lifepath_count, num_defs=3):
    '''
    Returns the n-max values of a dictionary.
    '''
    
    # Get the n-top max values
    max_vals = sorted(lifepath_count.values(), reverse=True)[:num_defs]
    
    # Assemble the output
    out_string = '\n'
    for key in sorted(lifepath_count.keys()):
        
        if lifepath_count[key] is max_vals[0]:
            out_string += '  * '
        else:
            out_string += '    '
        
        out_string += '%s - %d'%(str(key) if key != 0 else 'M', \
                                     lifepath_count[key],)
        if lifepath_count[key] in max_vals:
            out_string += '\t%s\n'%LIFEPATH_DEFS[key]
        else:
            out_string += '\n'
    
    # Print the output
    LOGGER.info(out_string) 

def sum_chars(input_number):
    '''
    Recursively sums the component numbers that make up the original until
    either a master number is reached or the number is between 0-9.

    ie.
    1984 -> 1+9+8+4 = 22          # Master number
    15   -> 1+5 = 6               # Single digit
    2008 -> 2008 = 10; 1+0 = 1    # Single digit
    '''
    
    if (input_number in MASTER_NUMBERS) or (len(str(input_number)) <= 1):
        return input_number
    else:
        return sum_chars(sum([int(i) for i in str(input_number)[:]]))

def process_file(filename):
    lifepath_count = defaultdict(int)
    in_file = open(filename, 'r')
    contents = reader(in_file, delimiter=',', quotechar='"')
    for row in contents:
        lifepath_num = date_to_number(row[1])
        if lifepath_num not in MASTER_NUMBERS:
            lifepath_count[lifepath_num] += 1
        else:
            lifepath_count[0] += 1
    return lifepath_count

def main():
    '''
    Main()
    '''
    
    # Open the file
    filename = './data/award_winner.csv'    
    lifepath_count = process_file(filename)
    log_result(lifepath_count)
    
if __name__ == '__main__':
    basicConfig(level=DEBUG)
    main()