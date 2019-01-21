# -*- coding: utf-8 -*- 
import os  
import json
import time
import sys



def matchLine(target,lines,index):
	if index >= len(lines):
		return -1
	timeprefix = lines[index].replace('.','').replace('\"','')[:11]
	
	
	
	if target < timeprefix:
		return -1
	
	while target != timeprefix:
		index += 1
		if index >= len(lines):
			return -1
		timeprefix = lines[index].replace('.','').replace('\"','')[:11]
		if target < timeprefix:
			return -1
	
	if target == timeprefix:
		return index
	else:
		return -1

if __name__ == "__main__":
	#id = 0
	if sys.argv[1]!=null and os.path.isdir(sys.argv[1]):
		dir = sys.argv[1]
	else:
		return
	#dir = "D:\\cicv\\BBB new data"
	#dir = "D:\\cicv\\AAAdata"
	fileList = os.listdir(dir)
	#print fileList
	
	for file in fileList:
		if not os.path.isdir(dir+"\\"+file):
			continue
		city = file.split('_')[0]
		
		#result data file
		resultFile = open(file+"_data.txt","w")
		
		result = []
		thisLine = {}
		thisLine['city'] = city
		
		#fieldList = ['can','gps','imu','road','obj','webp','pcl1_image','webp_marked']
		fieldList = ['can','gps','imu','webp','pcl1_image','webp_marked']
		"""
		fieldPaths = [
			"\\can\\can.csv",
			"\\imu\\gpsfix.csv",
			"\\imu\\imudata.csv",
			"\\me\\ivsensormeroad.csv",
			"\\me\\ivsensormeobj.csv",
			"\\webpList.csv",
			"\\pcl1_image.csv",
			"\\imageMarkedWebpList.csv"
		]
		"""
		fieldPaths = [
			"\\can\\can.csv",
			"\\imu\\gpsfix.csv",
			"\\imu\\imudata.csv",
			"\\image_webp.csv",
			"\\pcl1_imageList.csv",
			"\\image_marked_webp.csv"
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
		#roadFile.readline()
		#objFile.readline()
		
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
				
			
				
			tmp = matchLine(timeprefix,webpLines,webpLineIndex)
			if tmp == -1:
				continue
			else:
				webpData = ''
				webpLineIndex = tmp
				webpFields = webpLines[webpLineIndex][:-1].split(',')
				webpData = webpFields[1]
				webpLineIndex += 1
				
				
			tmp = matchLine(timeprefix,webp_markedLines,webp_markedLineIndex)
			if tmp == -1:
				continue
			else:
				webp_markedData = ''
				webp_markedLineIndex = tmp
				webp_markedFields = webp_markedLines[webp_markedLineIndex][:-1].split(',')
				webp_markedData = webp_markedFields[1]
				webp_markedLineIndex += 1
			
				
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
			json_str = json.dumps(thisLine)
			#id += 1
			#resultFile.write('{"index":{"_id":"'+str(id)+'"}}\n')
			resultFile.write(json_str+'\n')
			
			thisLine = {}
			thisLine['city'] = city
			
			#if len(result) >=300:
			#	print timeprefix
			#	break

		#rs = {"result":result}
		#json_str = json.dumps(rs)
		#resultFile.write(json_str)
		
		#close files
		for x in fieldList:
			exec(x+"File.close()")
		resultFile.close()
