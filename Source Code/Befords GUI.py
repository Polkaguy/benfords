print('Loading')
version = 'a.4'
print("Version:" + version)
import pandas as pd
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QWidget, QFileDialog, 
                            QLabel, QInputDialog, QPushButton, QMessageBox,
                            QMainWindow, QAction, QTableWidget, QTableWidgetItem,
                            QVBoxLayout, QAbstractItemView, QHeaderView)
from PyQt5.QtCore import pyqtSlot, Qt
from numpy import log10, nan, sqrt, floor
from matplotlib.backend_tools import ToolBase, ToolToggleBase
import matplotlib.pyplot as plt
plt.rcParams['toolbar'] = 'toolmanager'
from requests import post
from platform import uname

from scipy.stats import norm

test_mode = False

#################################
# DECLARATION FOR PYQT5 CLASSES #
#################################
class interface(QWidget):
    def __init__(self):
        super().__init__()
    def openFileNameDialog(self):
        fileName, ok = QFileDialog.getOpenFileName(self,"Select File for Analysis","",
            "All Files (*);;CSV File (*.csv *.tsv *.txt);;Excel File (*.xlsx)")
        if not ok:
            sys.exit()
        elif fileName:
            print(fileName)
            self.fileName = fileName
    def Select(self, Inst, Labels):
        item, ok = QInputDialog.getItem(self, "Select Columns", Inst, Labels,
                 0, False)
        if ok and item:
            self.selected = item
        elif not ok:
            sys.exit()
    def confirm(self,message,title='Confirm Total'):
        buttonReply = QMessageBox.question(self, title,message)
        
        if (buttonReply == QMessageBox.Yes):
            return True
        else:
            return False
    def inform(self,message):
        reply = QMessageBox.information(self, 'Information', message)
    def file_save(self):
        name, ok = QFileDialog.getSaveFileName(self, 'Save File')
        if name:
            print(name)
            self.fileName = name
            return ok
    def createTable(self,df):
       # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(df.shape[0])
        self.tableWidget.setColumnCount(df.shape[1])

        for i in range(df.shape[0]):

            # User
            item = QTableWidgetItem()
            item.setFlags(Qt.ItemIsSelectable |  Qt.ItemIsEnabled)
            item.setText(df.iloc[i,0])
            self.tableWidget.setItem(i,0,item)

            # Total Spending
            item = QTableWidgetItem()
            item.setFlags(Qt.ItemIsSelectable |  Qt.ItemIsEnabled)
            item.setText('${:,.2f}'.format(df.iloc[i,1]))
            self.tableWidget.setItem(i,1,item)

            # Number of transactions
            item = QTableWidgetItem()
            item.setFlags(Qt.ItemIsSelectable |  Qt.ItemIsEnabled)
            item.setText('{:,.0f}'.format(df.iloc[i,2]))
            self.tableWidget.setItem(i,2,item)

            # Max M
            item = QTableWidgetItem()
            item.setFlags(Qt.ItemIsSelectable |  Qt.ItemIsEnabled)
            item.setText('{:.4f}'.format(df.iloc[i,3]))
            self.tableWidget.setItem(i,3,item)
        self.tableWidget.setHorizontalHeaderLabels(['User','Transactions Total','Number of\nTransactions','p-value\n(Lower value = higher risk)'])
        
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        self.tableWidget.move(0,0)

        #Interface buttons 
        self.see_dist  = QPushButton('See distribution')
        self.see_dist.clicked.connect(self.on_click)

        self.save_results  = QPushButton('Save results')
        self.save_results.clicked.connect(save_result)

        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.layout.addWidget(self.see_dist)
        self.layout.addWidget(self.save_results)
        self.setLayout(self.layout) 
        # Header
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        # Show widget
        self.showMaximized()

    @pyqtSlot()
    def on_click(self):
        print("\n")
        try:
            row = []
            
            for currentQTableWidgetItem in self.tableWidget.selectedItems():
                if currentQTableWidgetItem.row() not in row:
                    row += [currentQTableWidgetItem.row()]
            if len(row) < 1: ex.inform('Please select user to graph.')
            for r in row:
                plotBenford(r)
            plt.show()

        except Exception as e:
            print("Error showing distribution.")
            print(e)
    # Save dialog


class popup(QWidget):
    def __init__(self):
        super().__init__()
    def inform(self,message):
        self.reply = QMessageBox.information(self, 'Information', message)

def bounds(n,alpha=.10)->([float],[float]):
    '''This function returns lists of the upper and lower bounds of the expected first
    significant digit distribution. '''
    upper = []
    lower = []
    def f_discrete_b(d): return log10(1+(1/d))
    for i in range(1,10):
        p = f_discrete_b(i)
        moe = sqrt((p * (1-p))/n) * norm.ppf(alpha/2)
        upper += [min(p+moe,1)]
        lower += [max(p-moe,0)]
    return (upper,lower)
##################################
# DECLARATION FOR GRAPHIC OUTPUT #
##################################

def plotBenford(row):
    '''Accepts an index number then creates a plot based on 
    the Benford's law analysis'''

    # Calculate actual distribution
    u = results.iloc[row,0]
    tdf = df[df['users']==u]
    
    vals = []
    amts = []
    for d in range(1,10):
        mask = (tdf['fsd']==d)
        vals += [mask.sum()/tdf.shape[0]]
        amts +=[tdf[mask]['amount'].sum()]

    # Calculate upper and lower bounds
    alpha = .10
    upper,lower = bounds(tdf.shape[0],alpha)
    
    f,ax = plt.subplots(1,1)
    
    # Create plot for total amounts
    ax2 = ax.twinx()
    ax2.plot(range(1,10),amts,'g_')
    ax2.set_ylim(bottom=0,top=max(amts)*1.2)
    ax2.legend(['Total amount of transactions\n(Not expected to fit distribution)'],loc='lower left')
    ax2.set_ylabel('Total amount of transaction')
    ax2.set_visible(False)
    # Plot actual distribution
    ax.plot(range(1,10),vals,'rx')

    # Plot bounds
    ax.plot(range(1,10),upper,'b')
    ax.plot(range(1,10),lower,'b')

    ax.legend(['Actual Distribution','Expected distribution (upper and lower bounds)'])
    ax.set_xlabel('First Significant Digit')

    ax.set_xticks(range(1,10))
    ax.set_ylabel('Number of Occurances')
    ax.set_ylim(bottom=0)
    ax.set_title(u)
    f.canvas.set_window_title(u)

    # Remove unnedded buttons
    f.canvas.manager.toolmanager.remove_tool('forward')
    f.canvas.manager.toolmanager.remove_tool('back')
    f.canvas.manager.toolmanager.remove_tool('home')
    f.canvas.manager.toolmanager.remove_tool('pan')
    f.canvas.manager.toolmanager.remove_tool('zoom')
    # Add custom buttons
    f.canvas.manager.toolmanager.add_tool('Dist. to Clipboard',dist_to_clip,{'list':vals,'user':u})
    f.canvas.manager.toolbar.add_tool('Dist. to Clipboard', 'navigation', 0)

    f.canvas.manager.toolmanager.add_tool('Transactions to Clipboard',trans_to_clip,{'user':u})
    f.canvas.manager.toolbar.add_tool('Transactions to Clipboard', 'navigation', 1)
    
    f.canvas.manager.toolmanager.add_tool('Show amount', show_amt, ax=ax2)
    f.canvas.manager.toolbar.add_tool('Show amount', 'navigation', 2)
    #f.canvas.manager.toolbar.add_tool('Show Amounts', show_amounts)
    #f.canvas.manager.toolmanager.add_tool('Show Amounts', 'navigation', 2)
    return
class trans_to_clip(ToolBase):
    '''Class to add custom button to Benford's distribution.
    see description for additional information.'''
    description='Save this users transactions to the clipboard for further analysis.\nYou can paste into your spreadsheet software.'
    def __init__(self,*args, gid=None, **kwargs):
        self.user = args[2]['user']
        self._name = 'Transactions to Clipboard'
    def trigger(self,*args):
        mask = full_df[params.loc['Users field','value']] == self.user
        
        # Handler for a large number of records
        if mask.sum() > 10000:
            message = 'There are {:,.0f} records, your computer might crash. <b>Conintue anyways</b>'.format(mask.sum())
            if not ex.confirm(message,"Warning: Large amount of data"): return None
        if full_df.index.name is None:
            full_df.index.name = 'Python index number'
        full_df[mask].to_clipboard()

        pu.inform('Copied '+str(self.user)+ ' transactions to clipboard.')
class dist_to_clip(ToolBase):
    '''Class to add custom button to Benford's distribution.
    see description for additional information.'''
    description = 'Copy the actual and expected distribution for the current user to the clipboard for futher anlaysis.\nYou can paste into your spreadsheet software.'
    def __init__(self, *args, gid=None, **kwargs):
        self.list = args[2]['list']
        self.user = args[2]['user']
        self._name = 'Dist. to Clipboard'
    def trigger(self,*args):
        pd.DataFrame(index=range(1,10),data={'FSD Occurnace':self.list,'Expected Distribution':[log10(1+1/d) for d in range(1,10)]}).to_clipboard()
        pu.inform('Copied '+str(self.user)+ ' distribution to clipboard.')
class show_amt(ToolToggleBase):
    '''Show lines with a given gid'''
    default_keymap = '$'
    description = 'Show total amount of transactions.'
    default_toggled = False
    def __init__(self, *args, gid=None, ax=None, **kwargs):
        self.gid = gid
        super().__init__(*args, **kwargs)
        self.ax = ax

    def enable(self, *args):
        self.ax.set_visible(True)
        self.figure.canvas.draw()

    def disable(self, *args):
        self.ax.set_visible(False)
        self.figure.canvas.draw()


#####################
# # LOGIC FOR UI/UX #
#####################

def getFile():
    while(True):
        ex.openFileNameDialog()
        try:
            if((ex.fileName[-5:]=='.xlsx') or (ex.fileName[-5:]=='.xls')):
                print('Opening Excel file')
                with pd.ExcelFile(ex.fileName) as xl:
                    if len(list(xl.sheet_names)) > 1:
                        ex.Select(Labels=list(xl.sheet_names), Inst='Pick the sheet that has your data.')
                        s = ex.selected
                    else:
                        s = xl.sheet_names[0]
                    df = xl.parse(s)
            elif(ex.fileName[-4:]in['.csv','.tsv','.txt']):
                print('Opening csv file')
                df = pd.read_csv(ex.fileName)
            else:
                assert(False), 'Unable to determine filetype.'
            break
        except Exception as e:
            pu.inform('Unable to read file. Please select file.')
            print(e)
    return df, ex.fileName

params = pd.DataFrame(columns=['value']) # Intialize df for storing analysis paramters
# Initialize interface
app = QApplication(sys.argv)
ex = interface() 
pu = popup()

def getNumbers(full_df):
    '''Prompt the user for the column with numeric data'''
    while(True):
        ex.Select(Labels=cols, Inst='Pick the column that contains transaction data.')
        amount = ex.selected
    
        try:
            if full_df[amount].dtypes == 'object':
                # If the chosen column was read as text, we need to convert it to string. This code handles some edge cases.
                # The try will ask about error handling if necessary.
                try:
                    vals = pd.to_numeric(full_df[amount].str.replace(r'[\$,\s]',''))
                except:
                    message = '''<b>There was an error importing your data.</b>

                    This happens because the field you selected as an amount contains
                    values the program cannot recognize as a number.

                    Do you want to <b>try to ignore rows that have errors</b>?
                    '''
                    if ex.confirm(message,'ERROR!'):
                        nas = full_df[amount].isna().sum()
                        vals = pd.to_numeric(full_df[amount].str.replace(r'[\$,\s]',''),errors='coerce')
                        nas = vals.isna().sum()-nas
                        if nas==0:
                            message = 'Completed without removing values.\nContinue?'
                        elif nas == 1:
                            message = '''
                            We had to remove <b>{:,.0f}</b> value ({:.2%} of data).\n
                            <b>Continue?</b>'''.format(nas,nas/vals.shape[0])
                        else:
                            message = '''
                            We had to remove <b>{:,.0f}</b> values ({:.2%} of data).\n
                            <b>Continue?</b>'''.format(nas,nas/vals.shape[0])
                            # Note: these are not actually removed until the math portion. The error message is
                            # included because they are marked for removal as nan values.
                        if not ex.confirm(message,'Coerece errors'): assert(False), 'User didn not continue.'
                            # User clicked no to Continue. User doesn't fix error, so trigger the larger error handler.
                        
                    else:
                        assert(False), 'User did not coerce' # This triggers a different exception handler because...
                        # in this case the user did NOT resolve the first error.

            else:
                vals = full_df[amount]

            # Dialog box to confirm
            message = 'Transaction total for selected field is ${:,.2f}.\nContinue?'.format(vals.sum())
            if ex.confirm(message):
                break
            else:
                print('No clicked. Restarting dialog.')
        except Exception as e:
            print('Please try again to load numeric data.')
            print(e)
    return vals, amount

def getUsers(full_df):
    '''Prompt user for information on transaction user data'''
    # Asks user for identifiying information
    cols.remove(params.loc['Amount field','value'])
    while(True):
        ex.Select(Labels=cols, Inst="Pick the column that identifies the users/merchants/employees you wish to analyze.")
        users = ex.selected
        try:
            u_val = full_df[users]
            # Dialog box to confirm
            message = 'There are {:,.0f} unique users/merchants/employees.\nContinue?'.format(u_val.unique().shape[0])
            if ex.confirm(message):
                break
            else:
                print('No clicked. Restarting dialog.')
        except Exception as e:
            print('Please try again to load numeric data.')
            print(e)
    return u_val, users
###################################
## START OF USER INTERFACE CODE  ##
###################################

if not test_mode:
    # Accept EULA
    EULA = 'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY\
    OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT\
    LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS\
    FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO\
    EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE\
    FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN\
    AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE\
    OR OTHER DEALINGS IN THE SOFTWARE.\n\n\
    Do you agree to the terms of this software?'

    if not ex.confirm(EULA,"End User Licence Agreement"): sys.exit()

    # Ask for stats about use:
    ask = 'Are you willing to share anonymous information about\
    your computer to improve this software and check for updates? (Not required)'
    if ex.confirm(ask,'(Optional) Opt-in for improvements.'):
        try:
            data = dict(
                version=version,
                system=str(uname())
            )
            r = post('http://www.persichitte.com/t/benford/',data=data)
            if r:
                if len(r.text) > 0:
                    ex.inform(r.text)
            else:
                ex.inform('Unable to connect:\n'+str(r))
        except Exception as e:
            ex.inform("Unable to connect.")
            print(e)

# Get file
if not test_mode:
    full_df, params.loc['source','value'] = getFile()
else:
    full_df = pd.read_csv('C://Users//202506//Downloads//Examples - Final Example (3).csv') # Fast load for troubleshooting

cols = list(full_df.columns) # Define columns for the next two menus.

# Asks for appropriate column then checks for numeric data
if not test_mode:
    vals, params.loc['Amount field','value'] = getNumbers(full_df)
else:
    vals, params.loc['Amount field','value'] = full_df['Amount'],'Amount' # Skip for troubleshooting


# Create a new dataframe for analyzing data
if not test_mode:
    u_val, params.loc['Users field','value'] = getUsers(full_df)
else:
    u_val, params.loc['Users field','value'] = full_df['User'],'User' # Fast track troubleshooting

# Create a simple dataframe for analysis
df = pd.DataFrame({'users':u_val,'amount':vals}).fillna(0)

############################################
## INITIALIZE RESUTS AND MATH FOR SOLVING ##
############################################

# Creates a results dataframe
results = df.groupby('users').agg(['sum','count'])
## Analyzes Benfords

## Find fisrt significant digit for all transactions

# Handler for values that are less than 1
vals = vals[abs(vals)>0]
if vals.min()<1:
    m=floor(log10(vals.min()))
else:
    m=0
fsd = (abs(df['amount'])*(10**m)).astype(str).str.slice(stop=1).astype(int)
df['fsd'] = fsd

mask = (df['fsd'] == 0)
df.drop(df.index[mask],inplace=True)

# Handler for values that are less than 1 for full data (primarily for exporting data)
try:
    full_df['First significant digit'] = fsd
except:
    print('Unable to find fsd for full dataset.')

def maxm(FSD: list)->float:
    '''
    This code accepsts a discrete list of leading digits and then returns the max M statistic.
    '''
    # Initialize variables
    n = len(FSD)
    
    
    # Creates discrete distribution for math.
    def f_discrete_b(d): return log10(1+(1/d))
    
    # Iterates through all values to calculate the the % occurances of the FSD and stored in 
    # list in FSD

    maxm = 0 # Initialized maxM
    # Iterates through each FSD to calculte M
    for i in range(1,10):
        # Uses formula based on  BENFORD’S LAW, FAMILIES OF DISTRIBUTIONS AND A TEST BASIS pg. 6
        # I break the formula to 2 lines of code for readability.
        # pFSDi is the probability of digit `i` as the first significant digit.
        pFSDi = sum([1 for x in FSD if x == i]) / n
        m = abs(pFSDi - f_discrete_b(i))
        # If M is the largest M, stores it as maxM
        if m > maxm:
            maxm = m
    return norm.pdf(maxm * sqrt(n))

# Calculate maxM for each user
results['p-value'] = nan
for u in results.index:
    vals = df[df['users']==u]['fsd'].values
    results.loc[u,'p-value'] = maxm(vals)

####################
## OUTPUT RESULTS ##
####################

# Format results for display
results = results.reset_index(drop=False).sort_values(by='p-value',ascending=True)


def save_result():
    '''
    This function prompts the user to save and handels the UI elements and error handling of 
    saving the outputs. It saves both the results and the parameters dataframe. They are 
    not called because they are mutable filetypes.
    '''
    ex.fileName=''
    ok = ex.file_save()

    if not ok:
        return
    if (ex.fileName[-5:]!='.xlsx'):
        ex.fileName = ex.fileName + ".xlsx"
    xl = pd.ExcelWriter(ex.fileName)
    results.to_excel(xl,'Amount by user')

    # Additional parameters
    params.loc['Time of analysis','value']=pd.Timestamp.now()
    params.loc['Robert Persichitte','value']='All rights reserved.'
    params.loc['Version','value']=version
    params.loc['Documentation','value']='http://persichitte.com/benfords/'
    params.to_excel(xl,'Paramters')

    xl.save()
    xl.close()
    ex.inform('Saved to' + ex.fileName)

ex.createTable(results)
sys.exit(app.exec_())
