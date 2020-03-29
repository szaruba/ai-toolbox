import matplotlib.pyplot as plt
import numpy as np
import csv

with open("../log/logfile.txt", "r") as f:
    reader = csv.reader(f, delimiter=';')

    log_values = []
    for i in range(8):
        log_values.append([])

    for i, row in enumerate(reader):
        print(row)
        if i == 0:
            continue

        log_values[0].append(int(row[0]))
        log_values[1].append(row[1])
        log_values[2].append(row[2])
        log_values[3].append(float(row[3]) if row[3] else 0)
        log_values[4].append(float(row[4]) if row[4] else 0)
        log_values[5].append(2 if row[5] == 'True' else 0 if row[5] == "False" else 1)
        log_values[6].append(float(row[6]) if row[6] else np.nan)
        log_values[7].append(float(row[7]) if row[7] else np.nan)

    print(log_values)

img_names = ["cat.0.jpg", "cat.1.jpg", "cat.2.jpg", "cat.3.jpg", "cat.4.jpg", "", "dog.0.jpg", "dog.1.jpg", "dog.2.jpg", "dog.3.jpg", "dog.4.jpg"]
img_labels = ["tiger cat", "tabby", "Siamese cat", "Egyptian cat", "", "Tibetan terrier", "Chesapeake Bay retriever", "Border collie", "Cardigan", "Labrador retriever"]

fig = plt.figure(figsize=(20,10))
sp5 = plt.subplot(515)
plt.title('CPG', loc="left")
plt.plot(log_values[0], log_values[6], label="Ant. M. Signal")
plt.plot(log_values[0], log_values[7], label="Post. M. Signal")
plt.legend(loc="right")

sp1 = plt.subplot(511, sharex=sp5)
# plt.yticks(np.arange(11), img_names)
# sp1.set_yticklabels(img_names)
plt.title('Environment', loc="left")
plt.plot(img_names, alpha=0, color='b')
plt.plot(log_values[0], log_values[1])
plt.setp(sp1.get_xticklabels(), visible=False)

sp2 = plt.subplot(512, sharex=sp5)
plt.title('Visual', loc="left")
plt.plot(img_labels, alpha=0, color='b')
plt.plot(log_values[0], log_values[2])
plt.setp(sp2.get_xticklabels(), visible=False)

sp3 = plt.subplot(513, sharex=sp5)
plt.title('Eval', loc="left")
plt.plot(log_values[0], log_values[3], "ro-", label="Danger", alpha=0.7)
plt.plot(log_values[0], log_values[4], "go-", label="Opportunity", alpha=0.7)
plt.legend(loc="right")
plt.setp(sp3.get_xticklabels(), visible=False)

sp4 = plt.subplot(514, sharex=sp5)
plt.title('RPG', loc="left")
plt.plot(log_values[0], log_values[5], label="Change Pattern")
plt.legend(loc="right")
plt.yticks(np.arange(3), ["False", "No Signal", "True"])
plt.setp(sp4.get_xticklabels(), visible=False)

plt.show()
