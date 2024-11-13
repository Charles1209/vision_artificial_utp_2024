import cv2
import os
import numpy as np
import sys
import subprocess
import platform

def detect_face(img):
	face_cascade_path = "src/lab6/Lab6_C_Files/opencv-files/lbpcascade_frontalface.xml"

	#convert the test image to gray image as opencv face detector expects gray images
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	
	#load OpenCV face detector, I am using LBP which is fast
	face_cascade = cv2.CascadeClassifier(face_cascade_path)

	#let's detect multiscale (some images may be closer to camera than others) images
	# the result is a list of faces
	faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
	
	#if no faces are detected then return original img
	if (len(faces) == 0):
		return None, None
	
	#under the assumption that there will be only one face, extract the face area
	(x, y, w, h) = faces[0]
	
	#return only the face part of the image
	return gray[y:y+w, x:x+h], faces[0]

#function to draw rectangle on image according to given (x, y) coordinates and given width and heigh
def draw_rectangle(img, rect):
	(x, y, w, h) = rect
	cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
	
#function to draw text on give image starting from passed (x, y) coordinates. 
def draw_text(img, text, x, y):
	cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

#this function recognizes the person in image passed
#and draws a rectangle around detected face with name of the subject
def predict(test_img, subjects):
	#make a copy of the image as we don't want to chang original image
	img = test_img.copy()

	#detect face from the image
	face, rect = detect_face(img)

	# mostrar imagen de prueba recortada
	cv2.imshow("Mostrando rostro de predicción", face)

	#predict the image using our face recognizer 
	label= face_recognizer.predict(face)

	print(label[1])  #valor de confidence, es una distancia entre más pequeño más cerca por lo tanto mejor

	#get name of respective label returned by face recognizer
	label_text = subjects[label[0]]
	
	#draw a rectangle around face detected
	draw_rectangle(img, rect)

	#draw name of predicted person
	draw_text(img, label_text, rect[0], rect[1]-5)
	
	return img

################################################################################################

def limpiar_consola():
	sistema = platform.system()
	
	if sistema == "Windows":
		os.system('cls')  # Comando para limpiar en Windows
	else:
		os.system('clear')  # Comando para limpiar en Linux y macOS

def verificar_persona():
	pass

# def insertar_persona(path_cropped_faces, faces, labels, names):
def insertar_persona(path_cropped_faces, labels, names):
	flag = False

	# def guardar_rostros(path_cropped_faces, faces, labels, names, flag, i):
	def guardar_rostros(path_cropped_faces, labels, names, flag, i):
		camara = cv2.VideoCapture(0)
		nombre = None
		faces = []
	
		while(True):
			_, frame = camara.read() # ret, frame = camara.read()
			cv2.imshow('Login Facial',frame) # Mostramos el video en pantalla
			if (cv2.waitKey(1) == 27) or (cv2.waitKey(1) & 0xFF == ord('q')): #Cuando oprimamos "Escape" o "q" rompe el video
				cv2.destroyAllWindows()
				camara.release() #Cerramos
				break
	
		rostro, _ = detect_face(frame)

		if rostro is not None:
			flag = True

			cv2.imshow("Rostro Detectado", rostro)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

			nombre = input("Ingrese un nombre para el nuevo usuario: ")

			if nombre in names:
				posicion = names.index(nombre)
				print(f"posicion: {posicion}")
				print(names)
				print(names[posicion])

				path_nombre_carpeta = path_cropped_faces + "/" + str(posicion)
				print(f"Carpeta encontrada en: {path_nombre_carpeta}")
				numero = os.listdir(path_nombre_carpeta)
				print(f"numero: {numero}")
				numero = len(numero)
				print(f"numero: {numero}")
				path_nombre_imagen = path_nombre_carpeta + "/" + str(numero+1) + ".png"
				labels.append(int(posicion))
			else:
				cantidad = os.listdir(path_cropped_faces)
				cantidad = len(cantidad)

				path_nombre_carpeta = path_cropped_faces + "/" + str(cantidad+1)
				os.makedirs(path_nombre_carpeta)
				path_nombre_imagen = path_nombre_carpeta + "/1.png"
				names.append(nombre)
				with open("src/proyecto/nombres.txt", "a") as file:
					file.write(f"\n{nombre}")
				labels.append(cantidad+1)

			# with np.load("src/proyecto/rostros.npz") as data:
			# 	faces = [data[key] for key in data.files]

			path_faces = "src/proyecto/rostros.npz"

			# Cargar imágenes existentes, si el archivo ya tiene contenido
			try:
				with np.load(path_faces) as data:
					faces = [data[key] for key in data.files]
				print("cargate!!!")
			except FileNotFoundError:
				# Si el archivo no existe, inicializar una lista vacía
				# faces = []
				pass

			# if len(faces) == 0:
			# 	np.savez("src/proyecto/rostros.npz", *faces)
			# 	# with open("src/proyecto/rostros.txt", "a") as file:
			# 	# 	file.write(str(rostro.astype(np.uint8)))
			# else:
			# 	with open("src/proyecto/rostros.txt", "a") as file:
			# 		file.write(f"\n...\n{str(rostro.astype(np.uint8))}")
			# print(faces)
			# print(type(faces))
			# faces.append(rostro.astype(np.uint8))
			faces.append(rostro)
			np.savez("src/proyecto/rostros.npz", *faces)

			cv2.imwrite(path_nombre_imagen, rostro)
		else:
			print(f"{i}. Rostro no detectado.")
			flag = False

		print(faces)
		return faces, labels, names, flag
	
	# def reconocer_rostros(faces, labels):
	def reconocer_rostros(faces, labels):
		face_recognizer = cv2.face.LBPHFaceRecognizer_create()

		print(faces)
		print(f"Que tengo en labels?\n{labels}")

		face_recognizer.train(faces, np.array(labels, dtype=np.int32))

	i=1
	while flag == False:
		# faces, labels, names, flag = guardar_rostros(path_cropped_faces, faces, labels, names, flag, i)
		faces, labels, names, flag = guardar_rostros(path_cropped_faces, labels, names, flag, i)
		i += 1
	
	reconocer_rostros(faces, labels)

def ver_identificados(path_cropped_faces):
	# Detectar el sistema operativo
	sistema = platform.system()
	
	if sistema == "Windows":
		os.startfile(path_cropped_faces)  # Para Windows
	elif sistema == "Linux":
		subprocess.run(['xdg-open', path_cropped_faces])  # Para Linux
	elif sistema == "Darwin":  # macOS
		subprocess.run(['open', path_cropped_faces])      # Para macOS

def funcion_init():
	# Variables importantes:
	# path_cropped_faces
	# faces
	# labels
	# names

	# Verificar la carpeta de los rostros
	path_cropped_faces = "src/proyecto/rostros"
	if not os.path.exists(path_cropped_faces):
		os.makedirs(path_cropped_faces)

	# Verficar el archivo donde guarda los nombres en números de los rostros
	# Verificar el archivo donde guarda los rostros en forma de matriz
	# path_faces = "src/proyecto/rostros.npz"
	# # Cargar imágenes existentes, si el archivo ya tiene contenido
	# try:
	# 	with np.load(path_faces) as data:
	# 		faces = [data[key] for key in data.files]
	# except FileNotFoundError:
	# 	# Si el archivo no existe, inicializar una lista vacía
	# 	faces = []

	# if not os.path.isfile(path_faces):
	# 	with open(path_faces, "w") as file:
	# 		pass
	# 	faces = []
	# else:
	# 	with open(path_faces, "r") as file:
	# 		words_from_file = [line.strip() for line in file.readlines()]
	# 	faces = words_from_file
	# faces = []
	# if os.path.isfile(path_faces):
	# 	with open(path_faces, "rb") as file:
	# 		for line in file.readlines():
	# 			faces.append(np.frombuffer(line, dtype=np.uint8))
		# 	words_from_file = [line.strip() for line in file.readlines()]  # Remove newline characters
		# 	words_from_file = file.read()
		# faces = np.frombuffer(words_from_file, dtype=np.uint8)
	
	# Verifica el archivo donde guarda el nombre de los rostros
	path_name_faces = "src/proyecto/nombres.txt"
	names = []
	if not os.path.isfile(path_name_faces):
		names.append("")
		with open(path_name_faces, "w") as file:
			file.write("")
	else:
		with open(path_name_faces, "r") as file:
			words_from_file = [line.strip() for line in file.readlines()]
		names = words_from_file

	# Programar para guardar en archivo y no tener que calcular
	# Verificar los archivos dentro de las carpetas de los rostros y los nombres de los rostros
	faces = [] # esto es tmp
	labels = []

	name_faces = os.listdir(path_cropped_faces)
	print(name_faces)
	
	for number_face in name_faces:
		print(f"Number face: {number_face}")
		path_number_file = path_cropped_faces + "/" + number_face
		print(path_name_faces)
		number_file = os.listdir(path_number_file)
		print(number_file)

		i = 1
		for file in number_file:
			if file.startswith("."):
				continue

			image_path = path_number_file + "/" + file
			print(image_path)

			image = cv2.imread(image_path)

			if image is None:
				print(f"Error loading image: {image_path}")
			else:
				face, _ = detect_face(image)

				if face is not None:
					faces.append(face)
					labels.append(i)
					print(f"Valor de i: {i}")

			i += 1
		
	#print(faces)
	#print(names)
	print(labels)
	
	# for img in faces:
	# 	cv2.imshow("Cargando rostros", img)
	# 	cv2.waitKey(100)
	# cv2.destroyAllWindows()
			
	# return path_cropped_faces, faces, labels, names
	return path_cropped_faces, labels, names

if __name__ == "__main__":
	path_cropped_faces, labels, names = funcion_init()

	while True:
		#limpiar_consola()
		print("\nBienvenido")
		print("\n1. Verificar persona.")
		print("2. Insertar persona.")
		print("3. Ver personas identificadas.")
		print("0. Salir.")
		opcion = int(input("\nInserte un número del menú: "))

		match opcion:
			case 0:
				#sys.exit("\nHasta Pronto.\n")
				print("\nHasta pronto.\n")
				break
			case 1:
				verificar_persona()
			case 2: 
				#insertar_persona(path_cropped_faces, faces, labels, names)
				insertar_persona(path_cropped_faces, labels, names)
			case 3:
				ver_identificados(path_cropped_faces)
			case _: 
				while (opcion < 0 or opcion > 3):
					print("Por favor inserte una opción válida.")
					opcion = int(input("\nInserte un número del menú: "))