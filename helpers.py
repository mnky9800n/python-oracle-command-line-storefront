


                               
import cx_Oracle, re



class gatherer:
            
    def getInput(self,prompt,regEx):
        validate = re.compile(regEx)
        input = raw_input(prompt)
        input.strip()
        while validate.match(input)==None:
            input = raw_input("Invalid input, try again:")
            input.strip()
        return input

#    def getNumber(self, prompt):
#        return = getInput(prompt,"\d+")
#
#    def getZip(self, prompt):
#        return = getInput(prompt,"\d{5}(-\d{4})?")
#
#    def getSSN(self, prompt):
#        return = getInput(prompt,"\d{3}-\d{2}-\d{5965}")


class dataSet:
    def __init__(self, connectionString, debug=False):
        if debug:
            print "You're using Oracle Client Tools v" + ".".join(map(str,cx_Oracle.clientversion()))
        self._conn = cx_Oracle.connect(connectionString)
        self._conn.autocommit = True
        self._curs = self._conn.cursor()
        self.fetchall = self._curs.fetchall
        self.description = self._curs.description
        self.columns = dict()

    def __del__(self):
        self._conn.close()

    def __iter__(self):
        return self._curs.__iter__()

   #Executes SQL statements   
    def execute(self, statement, **parameters):
        if parameters is None:
            self._curs.execute(statement)
        else:
            self._curs.execute(statement,parameters)

    #Creates a dictionary of column names and positions.
        if self._curs.description != None:
            self.columns = dict((field[0], pos) for pos, field in enumerate(self._curs.description))
        else:
            self.columns = None
   
    #Returns the column names of the last executed query as an ordered list
    def columnNames(self):
        import operator
        #make dict into list of tuples sorted by dict values
        cols = sorted(self.columns.iteritems(), key=operator.itemgetter(1))
        #make list into list of strings of the dict keys
        cols = [pair[0] for pair in cols]
        return cols