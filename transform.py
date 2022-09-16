import requests
import json
import config
import extract
from re import sub
import pandas as pd
from copy import deepcopy


class Pulldata(extract.Loading):
    def data_pull(self):
        #keys = ['general', 'images', 'videos', 'attachments', 'operational', 'dimensions', 'features', 'engine', 'drivetrain', 'electrical', 'options']
        #data_dict = {key: None for key in keys}       #defining the dictionary with keys and None type values
        general = {}
        images = []
        videos = []
        attachments = []
        operational = {}
        dimensions = {}
        features = []
        engine = {}
        drivetrain = {}
        electrical = {}
        options = []
        data_dict = {}
        data = []               #all the dictionaries needs to be appended into this list in the end
        ind_data = extract.Loading.industries(self)     #loading industries data
        category = [sub['title'] for sub in ind_data]
        node_ID = [sub['nodeID'] for sub in ind_data]

# looping through the other end points for rest of the data
#looping through product lines
        for nodes in range(len(node_ID)):
            for categories in range(nodes, len(category)):
                general['category'] = category[categories]
                break
            #print(general)
            general['manufacturer'] = "Vermeer"
            general['msrp'] = 0
            general['year'] = 2021
            general['countries'] = ["US"]
            product_lines_data = extract.Loading.fetchingproductlines(self, node_ID[nodes])
            industry_PL = [sub['industryProductLines'] for sub in product_lines_data]
            #print(industry_PL)
            industryProduct_line = []

            for i in industry_PL:
                for j in i:
                    industryProduct_line.append(j)
                    #print(industryProduct_line)
            rightnode = [sub['rightNodeId'] for sub in industryProduct_line]
            #subcategory = industryProduct_line[0]['documentName']
            subcategory = [sub['documentName'] for sub in industryProduct_line]
            #print(subcategory)

            # for subcategories in subcategory:
            #
            #     general['subcategory'] = subcategories
            #     a.append(general)
            #     print(a)
            #     general.clear()
            # print(a)
# looping through products via right node ID

            for nodes_right in range(len(rightnode)):
                for subcategories in range(nodes_right, len(subcategory)):
                    general['subcategory'] = subcategory[subcategories]
                    break
                #print(general)
                productss = extract.Loading.fetchingproducts(self, rightnode[nodes_right])
                nodeid = []
                model = []
                descriptiongeneral = []
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

                for id in range(len(nodeid)):
                    for models in range(id, len(model)):
                        general['model'] = model[models]
                        break
                    for description_general in range(id, len(descriptiongeneral)):
                        general['description'] = descriptiongeneral[description_general]
                        break
                    # ****************************************************
                    data_dict['general'] = general
                    # print(data_dict)
                    # *****************************************************
                    productdet = extract.Loading.fetchingproductdetails(self, nodeid[id])
                    #print(productdet)
                    #images = []
                    #videos = []

                    medias_1 = []
                    literatures_2 = []
                    #equipmentID = []

                    if productdet:
                        equipmentID = [sub['equipmentID'] for sub in productdet]
                        #equipmentID = productdet['equipmentID']
                        #print(equipmentID)
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
                        image_0['desc'] = ""
                        image_0['longdesc'] = ""
                        image_0['src'] = image0src
                        images.append(image_0)


                        for dict_of_medias in medias_1:
                            # dict_of_medias is a single dictionary from list of dictionary as in medias_1
                            if dict_of_medias['mediaType'] == 'Video':
                                videos_2 = {}
                                desc = dict_of_medias['title']
                                src = dict_of_medias['videoCode']
                                videos_2['desc'] = desc
                                videos_2['longdesc'] = ""
                                videos_2['src'] = src
                                videos.append(videos_2)
                        #print(videos)   #if print at this indent correct results
                            elif dict_of_medias['mediaType'] == 'Image':
                                images_1 = {}
                                desc = dict_of_medias['title']
                                src = dict_of_medias['image']
                                images_1['desc'] = desc
                                images_1['longdesc'] = ""
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
                            attachments_1['attachmentlongdescription'] = ""
                            attachments_1['attachmentSequence'] = ""
                            attachments.append(attachments_1)
                        #print(attachments)

# looping through specifications:
                    #for id_equipment in equipmentID:
                        data_dict['images'] = images
                        data_dict['videos'] = videos
                        data_dict['attachments'] = attachments
                        # for images_var in range(id_equipment, len(images)):
                        #     data_dict['images'] = images[images_var]
                        #     break
                        # for videos_var in range(id_equipment, len(videos)):
                        #     data_dict['videos'] = videos[videos_var]
                        #     break
                        # for attachments_var in range(id_equipment, len(attachments)):
                        #     data_dict['attachments'] = attachments[attachments_var]
                        #     break
                        #print(data_dict)

                        p_spec = extract.Loading.fetchingproductspecifications(self, equipmentID[0])
                        #print(p_spec)
                        if p_spec:
                            operational = {}
                            dimensions = {}
                            features = []
                            engine = {}
                            drivetrain = {}
                            electrical = {}
                            options = []

                            data_dict['operational'] = {}
                            data_dict['dimensions'] = {}
                            data_dict['features'] = []
                            data_dict['engine'] = {}
                            data_dict['drivetrain'] = {}
                            data_dict['electrical'] = {}
                            data_dict['options'] = []

                            for product_spec in p_spec:
                                if 'Dimensions' in product_spec['groupName'] or 'Capacities' in product_spec['groupName']:
                                    #dimensions = {}
                                    key_val = product_spec["specName"]
                                    primarydisplay = product_spec["primaryDisplayValue"]
                                    if primarydisplay is not None:
                                        spec = product_spec["specName"]
                                        key_value = Pulldata.camelCase(self, spec)
                                        sym = product_spec["primarySymbol"]
                                        if sym:
                                            text_value = primarydisplay + " " + sym
                                        else:
                                            text_value = primarydisplay
                                        text_sec = ""
                                        secondary_value = product_spec['secondaryDisplayValue']
                                        if secondary_value:
                                            sec_sym = product_spec['secondarySymbol']
                                            if sec_sym:
                                                text_sec = " ( " + secondary_value + " " + sec_sym + " )"
                                            else:
                                                text_sec = " ( " + secondary_value + " )"
                                        dimensions_1 = Pulldata.product_spec(self, key_val, key_value, text_value, text_sec)
                                        dimensions.update(dimensions_1)    #check this
                                        #temp = dimensions
                                    #     if dimensions:
                                    #         data_dict['dimensions'] = dimensions
                                    # else:
                                    #     continue
# need to correct this according to the format for group name features

                                elif product_spec['groupName'] == "Features":
                                    primarydisplay = product_spec["primaryDisplayValue"]
                                    if primarydisplay is not None:
                                        key = product_spec["specName"]
                                        features_1 = key + " - " + primarydisplay
                                        features.append(features_1)

                                elif 'Engine' in product_spec['groupName'] or 'Power Unit' in product_spec['groupName']:
                                    key_val = product_spec["specName"]
                                    primarydisplay = product_spec["primaryDisplayValue"]
                                    if primarydisplay is not None:
                                        spec = product_spec["specName"]
                                        key_value = Pulldata.camelCase(self, spec)
                                        sym = product_spec["primarySymbol"]
                                        if sym:
                                            text_value = primarydisplay + " " + sym
                                        else:
                                            text_value = primarydisplay
                                        text_sec = ""
                                        secondary_value = product_spec['secondaryDisplayValue']
                                        if secondary_value:
                                            sec_sym = product_spec['secondarySymbol']
                                            if sec_sym:
                                                text_sec = " ( " + secondary_value + " " + sec_sym + " )"
                                            else:
                                                text_sec = " ( " + secondary_value + " )"
                                        engine_1 = Pulldata.product_spec(self, key_val, key_value, text_value, text_sec)
                                        engine.update(engine_1)

                                elif 'Options' in product_spec['groupName']:
                                    primarydisplay = product_spec["primaryDisplayValue"]
                                    if primarydisplay is not None:
                                        key = product_spec["specName"]
                                        options_1 = key + " - " + primarydisplay
                                        options.append(options_1)


#need to do the format according to the features

                                elif 'Transmission System' in product_spec['groupName'] or 'Clutch' in product_spec['groupName'] or 'Drive System' in product_spec['groupName']:
                                    key_val = product_spec["specName"]
                                    primarydisplay = product_spec["primaryDisplayValue"]
                                    if primarydisplay is not None:
                                        spec = product_spec["specName"]
                                        key_value = Pulldata.camelCase(self, spec)
                                        sym = product_spec["primarySymbol"]
                                        if sym:
                                            text_value = primarydisplay + " " + sym
                                        else:
                                            text_value = primarydisplay
                                        text_sec = ""
                                        secondary_value = product_spec['secondaryDisplayValue']
                                        if secondary_value:
                                            sec_sym = product_spec['secondarySymbol']
                                            if sec_sym:
                                                text_sec = " ( " + secondary_value + " " + sec_sym + " )"
                                            else:
                                                text_sec = " ( " + secondary_value + " )"
                                        drivetrain_1 = Pulldata.product_spec(self, key_val, key_value, text_value, text_sec)
                                        drivetrain.update(drivetrain_1)
                                    #     if drivetrain:
                                    #         data_dict['drivetrain'] = drivetrain
                                    # else:
                                    #     continue

                                elif 'Electrical' in product_spec['groupName'] or 'Mill Motor' in product_spec['groupName']:
                                    key_val = product_spec["specName"]
                                    primarydisplay = product_spec["primaryDisplayValue"]
                                    if primarydisplay is not None:
                                        spec = product_spec["specName"]
                                        key_value = Pulldata.camelCase(self, spec)
                                        sym = product_spec["primarySymbol"]
                                        if sym:
                                            text_value = primarydisplay + " " + sym
                                        else:
                                            text_value = primarydisplay
                                        text_sec = ""
                                        secondary_value = product_spec['secondaryDisplayValue']
                                        if secondary_value:
                                            sec_sym = product_spec['secondarySymbol']
                                            if sec_sym:
                                                text_sec = " ( " + secondary_value + " " + sec_sym + " )"
                                            else:
                                                text_sec = " ( " + secondary_value + " )"
                                        electrical_1 = Pulldata.product_spec(self, key_val, key_value, text_value, text_sec)
                                        electrical.update(electrical_1)
                                        # if electrical not in data_dict['electrical']:
                                        #     data_dict['electrical'] = electrical
                                    #     if electrical:
                                    #         data_dict['electrical'] = electrical
                                    # else:
                                    #     continue

                                else:
                                    key_val = product_spec["specName"]
                                    primarydisplay = product_spec["primaryDisplayValue"]
                                    if primarydisplay is not None:
                                        spec = product_spec["specName"]
                                        key_value = Pulldata.camelCase(self, spec)
                                        sym = product_spec["primarySymbol"]
                                        if sym:
                                            text_value = primarydisplay + " " + sym
                                        else:
                                            text_value = primarydisplay
                                        #adding secondary value also in the desc
                                        text_sec = ""
                                        secondary_value = product_spec['secondaryDisplayValue']
                                        if secondary_value:
                                            sec_sym = product_spec['secondarySymbol']
                                            if sec_sym:
                                                text_sec = " ( " + secondary_value + " " + sec_sym + " )"
                                            else:
                                                text_sec = " ( " + secondary_value + " )"
                                        operational_1 = Pulldata.product_spec(self, key_val, key_value, text_value, text_sec)
                                        operational.update(operational_1)
                                    #     if operational:
                                    #         data_dict['operational'] = operational
                                    # else:
                                    #     continue
                            #if dimensions:
                            data_dict['dimensions'] = dimensions
                            #if features:
                            data_dict['features'] = features
                            #if engine:
                            data_dict['engine'] = engine
                            #if options:
                            data_dict['options'] = options
                            #if drivetrain:
                            data_dict['drivetrain'] = drivetrain
                            #if electrical:
                            data_dict['electrical'] = electrical
                            #if operational:
                            data_dict['operational'] = operational


                            #print("***********")
                            data_dict = {k: v for k, v in data_dict.items() if v}
                            print(data_dict)

                            data.append(deepcopy(data_dict))
                            #data.update(data_dict)
                            #clear data_dict here

                    #print(data_dict)
                            #print(data_dict)
                    # for k,v in data_dict.items():
                    #     if data_dict[k]:
                    #         data.append(data_dict)
                    #print(data)


                            # if data_dict in data:
                            #     continue
                            # else:

                            #     data.append(data_dict)
        with open('json_output_3.json', 'w', encoding='utf8') as json_file:
            json.dump(data, json_file, indent=6, ensure_ascii=False)

        #print(data)

                            # if features:
                            #     print(features)
                            #
                            # if options:
                            #     print(options)
                            #print(operational)

            #print(general)

    # key_value is the key of label and desc
    #key_val is the value of spec name
    #text_value is the value of primary display value and its unit or symbol
    #text_sec is the secondary text value

    def product_spec(self, key_val, key_value, text_value, text_sec):
        specs = {}
        specs[key_value] = {}
        specs[key_value]["label"] = key_val
        specs[key_value]["desc"] = text_value + text_sec
        return specs

    def camelCase(self, spec):
        spec = spec.replace(" ", "")
        key_value = ''.join([spec[0].lower(), spec[1:]])
        return key_value


ayush = Pulldata()
ayush.data_pull()


