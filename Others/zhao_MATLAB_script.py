import xlrd



class Zhao():
    def getFileIndex(self):

        ofn = r'/Users/Zyang/Desktop/zhao/out.txt'
        outfile = open(ofn, 'wb')

        data = xlrd.open_workbook('/Users/Zyang/Desktop/zhao/a.xls')
        table = data.sheets()[0]
        nrows = table.nrows
        ncols = table.ncols

        fileIndexList = []
        indexY = 0.0

        for i in range(nrows):
            indexX = 0.0
            indexXList = []
            list = []
            if i % 2 == 0:
                row_values = table.row_values(i)
            else:
                row_values = table.row_values(i)[::-1]

            for j in range(ncols):
                indexXList.append(indexX)
                if i % 2 == 0:
                    list = indexXList
                else:
                    list = indexXList[::-1]
                indexX += 0.5



            for j in range(len(list)):
                insertContent = 'G90\nG00 X' + str(list[j]) + ' Y-' + str(indexY) + ' Z0.5\n'
                if int(row_values[j]) == 8:
                    outfile.write(insertContent)
                else:
                    ifn = r'/Users/Zyang/Desktop/zhao/' + str(int(row_values[j])) + '.txt'
                    infile = open(ifn, 'rb')
                    outfile.write(insertContent)
                    outfile.write(infile.read()+'\n')
                    infile.close()
                print insertContent
            indexY += 0.5
        outfile.close()


zhao = Zhao()
zhao.getFileIndex()
