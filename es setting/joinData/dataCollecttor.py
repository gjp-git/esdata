# -*- coding: utf-8 -*- 
import os  
import json
import time




def matchLine(target,lines,index):
	if index >= len(lines):
		return -1
	timeprefix = lines[index].replace('.','')[:11]
	
	if target < timeprefix:
		return -1
	
	while target != timeprefix:
		index += 1
		if index >= len(lines):
			return -1
		timeprefix = lines[index].replace('.','')[:11]
		if target < timeprefix:
			return -1
	
	if target == timeprefix:
		return index
	else:
		return -1

if __name__ == "__main__":
	#id = 0
	dir = "D:\\cicv\\BBB new data"
	fileList = os.listdir(dir)
	#print fileList
	
	for file in fileList:
		city = file.split('_')[0]
		
		#result data file
		resultFile = open(file+"_data.txt","w")
		
		result = []
		thisLine = {}
		thisLine['city'] = city
		
		fieldList = ['can','gps','imu','road','obj','image','webp','image_marked','pcl1','pcl1_image','webp_marked']
		fieldPaths = [
			"\\can\\can.csv",
			"\\imu\\gpsfix.csv",
			"\\imu\\imudata.csv",
			"\\me\\ivsensormeroad.csv",
			"\\me\\ivsensormeobj.csv",
			"\\imageList.csv",
			"\\webpList.csv",
			"\\imageMarkedList.csv",
			"\\pcl1.csv",
			"\\pcl1_image.csv",
			"\\imageMarkedWebpList.csv"
		]

		
		#open files
		#map(lambda x: exec(compile(fieldList[x]+'File = open(dir+"\\"+file+"'+fieldPaths[x]+'","r")', '<string>', 'exec')),[x for x in range(len(fieldList))])
		for x in range(len(fieldList)):
			cmd = fieldList[x]+'File = open("'+dir+'\\\\'+file+fieldPaths[x]+'","r")'
			exec(cmd)	
		
		#ingore first line
		canFile.readline()
		gpsFile.readline()
		imuFile.readline()
		roadFile.readline()
		objFile.readline()
		
		#read files
		for x in fieldList:
			exec(x+"Lines = "+x+"File.readlines()")

		#init line index
		for x in fieldList:
			exec(x+"LineIndex = 0")
		
		for canLine in canLines:
			canLine = canLine[:-1]
			canFields = canLine.split(',')
			timeprefix = canFields[0][:11]
			#print timeprefix
			thisLine["timestamp"] = timeprefix
			thisLine["time"] = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(int(timeprefix[:-1])))
			canData = {}
			canData['siVehicleSpeed'] = canFields[1]
			canData['siSteeringAngle'] = canFields[2]
			canData['siSteeringVelocity'] = canFields[3]
			canData['siBrakePressure'] = canFields[-5]
			canData['siAccelerationPedal'] = canFields[-1]
			
			tmp = matchLine(timeprefix,gpsLines,gpsLineIndex)
			#print tmp
			if tmp == -1:
				continue
			else:
				gpsData = {}
				gpsLineIndex = tmp
				gpsFields = gpsLines[gpsLineIndex][:-1].split(',')
				gpsData['latitude'] = gpsFields[6]
				gpsData['longitude'] = gpsFields[7]
				gpsData['altitude'] = gpsFields[8]
				location = {}
				location['lat'] = gpsFields[6]
				location['lon'] = gpsFields[7]
				gpsData['location'] = location
				gpsLineIndex+=1
				
			tmp = matchLine(timeprefix,imuLines,imuLineIndex)
			if tmp == -1:
				continue
			else:
				imuData = {}
				imuLineIndex = tmp
				imuFields = imuLines[imuLineIndex][:-1].split(',')
				imuData['orientation_x'] = imuFields[4]
				imuData['orientation_y'] = imuFields[5]
				imuData['orientation_z'] = imuFields[6]
				imuData['angular_velocity_x'] = imuFields[17]
				imuData['angular_velocity_y'] = imuFields[18]
				imuData['angular_velocity_z'] = imuFields[19]
				imuData['linear_acceleration_x'] = imuFields[29]
				imuData['linear_acceleration_y'] = imuFields[30]
				imuData['linear_acceleration_z'] = imuFields[31]
				imuLineIndex += 1
				
			tmp = matchLine(timeprefix,roadLines,roadLineIndex)
			if tmp == -1:
				continue
			else:
				roadData = {}
				roadLineIndex = tmp
				roadFields = roadLines[roadLineIndex][:-1].split(',')
				roadData['leftType'] = roadFields[1]
				roadData['righType'] = roadFields[2]
				roadData['curvature'] = roadFields[5]
				roadData['heading'] = roadFields[6]
				roadData['leftOffset'] = roadFields[7]
				roadData['rightOffset'] = roadFields[8]
				roadLineIndex += 1
				
			tmp = matchLine(timeprefix,objLines,objLineIndex)
			if tmp == -1:
				continue
			else:
				objData = []
				objLineIndex = tmp
				objFields = objLines[objLineIndex][:-1].split(',')
				num = len(objFields)//9

				if objFields[-1]=='1' and len(objFields)%9==2:
					for i in range(num):
						obj = {}
						obj['id'] = objFields[i*9+1]
						obj['x'] = objFields[i*9+2]
						obj['y'] = objFields[i*9+3]
						obj['relspeed'] = objFields[i*9+4]
						obj['width'] = objFields[i*9+5]
						obj['length'] = objFields[i*9+6]
						obj['height'] = objFields[i*9+7]
						obj['classification'] = objFields[i*9+9]
						objData.append(obj)
				else:
					print timeprefix+" obj failed"
				objLineIndex += 1
			
			tmp = matchLine(timeprefix,imageLines,imageLineIndex)
			if tmp == -1:
				continue
			else:
				imageData = ''
				imageLineIndex = tmp
				imageFields = imageLines[imageLineIndex][:-1].split(',')
				imageData = imageFields[1]
				imageLineIndex += 1
				
			tmp = matchLine(timeprefix,webpLines,webpLineIndex)
			if tmp == -1:
				continue
			else:
				webpData = ''
				webpLineIndex = tmp
				webpFields = webpLines[webpLineIndex][:-1].split(',')
				webpData = webpFields[1]
				webpLineIndex += 1
				
			tmp = matchLine(timeprefix,image_markedLines,image_markedLineIndex)
			if tmp == -1:
				continue
			else:
				image_markedData = ''
				image_markedLineIndex = tmp
				image_markedFields = image_markedLines[image_markedLineIndex][:-1].split(',')
				image_markedData = image_markedFields[1]
				image_markedLineIndex += 1
				
			tmp = matchLine(timeprefix,webp_markedLines,webp_markedLineIndex)
			if tmp == -1:
				continue
			else:
				webp_markedData = ''
				webp_markedLineIndex = tmp
				webp_markedFields = webp_markedLines[webp_markedLineIndex][:-1].split(',')
				webp_markedData = webp_markedFields[1]
				webp_markedLineIndex += 1
			
			tmp = matchLine(timeprefix,pcl1Lines,pcl1LineIndex)
			if tmp == -1:
				continue
			else:
				pcl1Data = ''
				pcl1LineIndex = tmp
				pcl1Fields = pcl1Lines[pcl1LineIndex][:-1].split(',')
				pcl1Data = pcl1Fields[1]
				pcl1LineIndex += 1
				
			tmp = matchLine(timeprefix,pcl1_imageLines,pcl1_imageLineIndex)
			if tmp == -1:
				continue
			else:
				pcl1_imageData = ''
				pcl1_imageLineIndex = tmp
				pcl1_imageFields = pcl1_imageLines[pcl1_imageLineIndex][:-1].split(',')
				pcl1_imageData = pcl1_imageFields[1]
				pcl1_imageLineIndex += 1
			
			#value thisline
			for x in fieldList:
				exec("thisLine['"+x+"'] = "+x+"Data")
		
			result.append(thisLine)
			#json_str = json.dumps(thisLine)
			#id += 1
			#resultFile.write('{"index":{"_id":"'+str(id)+'"}}\n')
			#resultFile.write(json_str+'\n')
			
			thisLine = {}
			thisLine['city'] = city
			
			#if len(result) >=300:
			#	print timeprefix
			#	break

		rs = {"result":result}
		json_str = json.dumps(rs)
		resultFile.write(json_str)
		
		#close files
		for x in fieldList:
			exec(x+"File.close()")
		resultFile.close()
