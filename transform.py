import requests
import json
import config
import extract
from re import sub

class Pulldata(extract.Loading):
    def data_pull(self):
        keys = ['general', 'images', 'videos', 'attachments', 'operational', 'dimensions', 'features']
        data_dict = {key: None for key in keys}       #defining the dictionary with keys and None type values
        data = []               #the dictionary needs to be appended into this list in the end
        ind_data = extract.Loading.industries(self)     #loading industries data
        title_values = [sub['title'] for sub in ind_data]
        node_ID = [sub['nodeID'] for sub in ind_data]

# looping through the other end points for rest of the data
#looping through product lines
        for nodes in node_ID:
            product_lines_data = extract.Loading.fetchingproductlines(self, nodes)
            industry_PL = [sub['industryProductLines'] for sub in product_lines_data]
            #print(industry_PL)
            industryProduct_line = []

            for i in industry_PL:
                for j in i:
                    industryProduct_line.append(j)
                    #print(industryProduct_line)
            rightnode = [sub['rightNodeId'] for sub in industryProduct_line]
            subcategory = [sub['documentName'] for sub in industryProduct_line]

# looping through products via right node ID
            for nodes in rightnode:
                productss = extract.Loading.fetchingproducts(self, nodes)
                nodeid = []
                model = []
                if productss:
                    products_data = [sub['products'] for sub in productss]
                    products_d = []

                    for i in products_data:
                        for j in i:
                            products_d.append(j)
                    nodeid = [sub['nodeID'] for sub in products_d]
                    model = [sub['title'] for sub in products_d]
                    descriptiongeneral = [sub['description'] for sub in products_d]
                    #print(nodeid)
                    #print(model)

#looping through product details via nodeid for the details of products

                for id in nodeid:
                    productdet = extract.Loading.fetchingproductdetails(self, id)
                    #images = []
                    #videos = []
                    equipmentID = []
                    #attachment = []
                    medias_1 = []
                    literatures_2 = []
                    equipmentID = None

                    if productdet:
                        equipmentID = [sub['equipmentID'] for sub in productdet]
                        image0src = [sub['baseImage'] for sub in productdet]
                        medias = [sub['medias'] for sub in productdet]
                        literature_1 = [sub['literatures'] for sub in productdet]
                        #print(medias)

                        for i in medias:
                            for j in i:
                                medias_1.append(j)
                        images = []
                        videos = []
                        image_0 = {}
                        image_0['desc'] = ''
                        image_0['longdesc'] = ''
                        image_0['src'] = image0src
                        images.append(image_0)


                        for dict_of_medias in medias_1:
                            # dict_of_medias is a single dictionary from list of dictionary as in medias_1
                            if dict_of_medias['mediaType'] == 'Video':
                                videos_2 = {}
                                desc = dict_of_medias['title']
                                src = dict_of_medias['videoCode']
                                videos_2['desc'] = desc
                                videos_2['longdesc'] = ''
                                videos_2['src'] = src
                                videos.append(videos_2)
                        #print(videos)   #if print at this indent correct results
                            elif dict_of_medias['mediaType'] == 'Image':
                                images_1 = {}
                                desc = dict_of_medias['title']
                                src = dict_of_medias['image']
                                images_1['desc'] = desc
                                images_1['longdesc'] = ''
                                images_1['src'] = src
                                images.append(images_1)
                        #print(images)

                        for i in literature_1:
                            for j in i:
                                literatures_2.append(j)
                        #literature 2 is the list of attachments
                        attachments = []

                        for dict_attachment in literatures_2:

                            attachments_1 = {}
                            attchmentdescription = dict_attachment['title']
                            literatureloc = dict_attachment['literatureItem']
                            attachments_1['attachmentDescription'] = attchmentdescription
                            attachments_1['attachmentLocation'] = literatureloc
                            attachments_1['attachmentlongdescription'] = ''
                            attachments_1['attachmentSequence'] = ''
                            attachments.append(attachments_1)
                        print(attachments)

# looping through specifications:
                    for id in equipmentID:
                        p_spec = extract.Loading.fetchingproductspecifications(self, id)




                        if p_spec:
                            for product_spec in p_spec:
                                if product_spec['groupName'] == "Discharge System" or "Processing System" or "Tub" or "Tractor Requirements":
                                    operational = {}
                                    key_val = product_spec["specName"]
                                    text_value = product_spec["textValue"]
                                    spec = product_spec["specName"]
                                    spec = spec.replace(" ", "")
                                    key_value = ''.join([spec[0].lower(), spec[1:]])
                                    operational_1 = Pulldata.product_spec_oper(self, key_val, key_value, text_value)
                                    operational.update(operational_1)


                                    #operational = {}

                                    # if product_spec['specName'] == "PTO horsepower minimum":
                                    #     operational["ptoHorsePower"] = {}
                                    #     operational['ptoHorsePower']['label'] = product_spec['specName']
                                    #     operational['ptoHorsePower']['desc'] = product_spec['textValue']
                                    #
                                    # if product_spec['specName'] == "Hydraulic flow rate":
                                    #     operational['Hydraulic flow rate'] = {}
                                    #     operational['Hydraulic flow rate']['label'] = product_spec['specName']
                                    #     operational['Hydraulic flow rate']['desc'] = product_spec['textValue']

    def product_spec_oper(self, key_val, key_value, text_value):
        operational = {}
        operational[key_value] = {}
        operational[key_value]["label"] = key_val
        operational[key_value]["desc"] = text_value
        return operational


                                    # ptoHorsePowermin = product_spec['PTO horsepower minimum']
                                    # hydraulicflowrate = product_spec['Hydraulic flow rate']
                                    # hydraulicpressure = product_spec['Hydraulics Pressure']

















                                        # for videos_key, videos_values in dict_of_medias.items():
                                        #     #print(videos_values)
                                        #     videos_2['desc'] = videos_key['title']
                                        #     videos_2['longdesc'] = ''
                                        #     videos_2['src'] = videos_key['videocode']
                                        #     #print(videos_2)


                                #[d['value'] for d in l if 'value' in d]









ayush = Pulldata()
ayush.data_pull()


