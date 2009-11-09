import backupAnt as ant, backupHelen as helen
import threading as tt

antThread = tt.Thread(target=ant.backup)
helThread = tt.Thread(target=helen.backup)

helThread.start()
antThread.start()
