import os

def read_method_details():
    

    with open("Collected_Data"+ os.path.sep + "Collected_Data.txt",'r' ) as fp:
         collector_data = fp.read()
    fp.close()
    with open("Cluster_Folder" + os.path.sep + "cluster_details.txt",'r') as gp:
        cluster_details = gp.read()
    gp.close()
    with open("classify_details.txt",'r') as dp:
        classify_details = dp.read()
    dp.close()

    with open("summary.txt",'w') as sp:
        sp.write("❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂\n\n")
        sp.write("**************All the reports and detail files were derived from their ___.py file on run time**************\n\n ")

        sp.write("Collector.py Details : \n\n")
        sp.write(collector_data)
        sp.write("Cluster.py Details : \n\n")
        sp.write(cluster_details)
        sp.write("Classify.py Details : \n\n")
        sp.write(classify_details)
        sp.write("❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂❂")

    sp.close()

    print("Details saved to --> summary.txt")

    return collector_data,cluster_details,classify_details


def main():

  

    collector_details,cluster_details,classify_details  = read_method_details()
   
    


if __name__ == main():
    main()
