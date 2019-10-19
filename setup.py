###

# Imports
import Settings as S

eventsGroup = 'GoogleCalSyncHABEvents'
fieldsGroup = 'GoogleCalSyncHABFields'
fields = ['summary','location','description','startDate','startTime','endDate','endTime','allDay','multipleDays']

def createItemsFile():
    # Creating items file
    with open('GoogleCalSyncHAB.items', 'wt') as items:
        items.writelines('////\n// Autogenerated items file.\n////\n\n// JSON event items\nGroup '+eventsGroup+'\n')
        for index in range(int(S.CalendarMaxEvents)):
            items.write('String\t' + S.OpenHABItemPrefix + 'Event' + str(index + 1) + '\t('+eventsGroup+')\n')

        items.writelines('\n\n// Calendar event field items\nGroup '+eventsGroup+'\n')
        for index in range(int(S.CalendarMaxEvents)):
            items.write('\n// Event' + str(index + 1) + '\n')
            for field in fields:
                items.write('String\t' + S.OpenHABItemPrefix + 'Event' + str(index + 1) + field + '\t('+fieldsGroup+')\n')
            # items.write('\n')

        items.writelines('\n\n\n////\n// End autogenerated items file.\n////\n\n')

def createRulesFile():
    # Creating items file
    with open('GoogleCalSyncHAB.rules', 'wt') as items:

        items.writelines('////\n// Autogenerated rules file.\n////\n\n')

        for index in range(int(S.CalendarMaxEvents)):
            items.write('\n// Event' + str(index + 1) + ' rule\n')
            itemRef = S.OpenHABItemPrefix + 'Event' + str(index + 1)
            items.write('rule "Convert calendar event' + str(index + 1) 
            + ' json to field items"\n\twhen\n\t\tItem\t' + itemRef 
            + '\treceived command\n\tthen\n\t\t// use the transformation service to retrieve the value\n')
            items.write('\t\tlogInfo("GoogleCalSync", "Refreshing Calendar_Google_Home_Event'+str(index + 1)+'")\n')
            for field in fields:
                fieldRef = S.OpenHABItemPrefix + 'Event' + str(index + 1) + field
                items.write('\t\tval value' + fieldRef + ' = transform("JSONPATH", "$.'+field+'", '+itemRef+'.state.toString)\n')
                items.write('\t\t' + fieldRef + '.postUpdate(value'+fieldRef+')\n')
            items.write('\n\tend\n')

        items.writelines('\n\n\n////\n// End autogenerated items file.\n////\n\n')

def main():
    createItemsFile()
    createRulesFile()



if __name__ == '__main__':
    main()