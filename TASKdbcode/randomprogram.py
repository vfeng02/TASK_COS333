import sys
import pandas
import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import functions
from demographic_db import get_patrons
import pickle

def main():
    x = get_patrons()
    filename = 'entries'
    outfile = open(filename,'wb')
    pickle.dump(x,outfile)
    outfile.close()
    infile = open(filename,'rb')
    new_dict = pickle.load(infile)
    infile.close()
    print(new_dict)

if __name__ == "__main__": 
    main()