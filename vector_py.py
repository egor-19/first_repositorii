#вектор

import ctypes

#massiv = (ctypes.c_int*10)() #массив из 10 эл-ов


from random import randint


class Vector:
    def __init__(self):
        self.length = 10
        self.occupied = 0
        self.massiv = (ctypes.c_int*self.length)()

    def __getitem__(self, number):
        if type(number) == int:
            return self.massiv[number]
        else:  
            new = Vector()
            
            start = number.start
            stop = number.stop
            step = number.step
            
            if start is None:
                start = 0
            
            if stop is None:
                stop = self.occupied
            
            if step is None:
                step = 1
        
            for i in range(start, stop, step):
                new.append(self.massiv[i])
            
            return new
                

    def __len__(self):
        return self.occupied
    #------------------------------
    def __setitem__ (self,index,item): 
        if 0<=index<=self.occupied-1:
            self.massiv[index] = item
        else:
            raise IndexError ("нет элемента по такому индексу")
        
    def __contains__ (self,item):
        for i in range(0,self.occupied):
            if self.massiv[i] == item:
                return True
        return False
    
    def __iter__(self):
        for i in range (0, self.occupied):
            yield self.massiv[i]

    def __str__ (self):
        #stroka = [str(self.massiv[i]) for i in range(self.occupied)]
        #return '['+','.join(stroka)+']'
        stroka='['
        for i in range(self.occupied-1):
            stroka+=str(self.massiv[i])+','
            
        return stroka +str(self.massiv[self.occupied-1])+']'
    
    def __eq__(self,other_vector):
        if not isinstance(other_vector,Vector):
            return False
        if self.occupied!= len(other_vector):
            return False
        for i in range(self.occupied):
            if self.massiv[i]!=other_vector[i]:
                return False
            
        return True
    
    def __add__(self, other_vector):
        if not isinstance(other_vector,Vector):
            raise TypeError ("разные типы! нельзя")
        new = self.copy()
        new.extend(other_vector)
        return new



    def __iadd__(self, other_vector):
        if not isinstance(other_vector,Vector):
            raise TypeError ("разные типы! нельзя")
        self.extend(other_vector)
        return self

    def __mul__ (self,n):
        new = Vector()
        for i in range (n):
            new.extend(self)

        return new

    def __delitem__(self, index):
        self.pop(index)

    def __reversed__(self):
        for i in range(self.occupied - 1, -1, -1):
            yield self.massiv[i]
        
    def __ne__(self, other):
        return not self.__eq__(other)
    

    def increase_memory (self):
        if self.occupied >= self.length:
            old_mass = self.massiv
            self.length*=2
            self.massiv = (ctypes.c_int*self.length)()
            for i in range(self.occupied):
                self.massiv[i]=old_mass[i]


    def clear(self):
        self.occupied = 0
        self.length = 10
        self.massiv = (ctypes.c_int*self.length)()


    def pop (self, index=-1):
        if self.occupied == 0:
            raise IndexError("массив пуст! Нечего удалять")
        
        if index == -1:
            index+=self.occupied

        if index<0 or index>=self.occupied:
            raise IndexError("Неверный индекс. Его значение не попадает в нужный диапазон")
        
        old_massiv = self.massiv
        self.occupied -=1
        self.massiv = (ctypes.c_int*self.length)()

        for i in range(0,index):
            self.massiv[i] = old_massiv[i]

        for i in range(index,self.occupied):
            self.massiv[i] = old_massiv[i+1]

        return old_massiv[index]
    

    def remove (self,value): #аходит первое вхождение значения value и удаляет его. Ничего не возвращает
        for i in range(0,self.occupied):
            if self.massiv[i]==value:
                self.pop(i)
                return value
        
        raise ValueError("такого значения в списке нет")
    

    def insert(self,index,value): #Вставляет новый элемент value на позицию index, сдвигая существующие элементы вправо.
        if index < 0 or index > self.occupied:  
            raise IndexError("Неправильный индекс")
        
        self.increase_memory()
        
        for i in range(self.occupied,index,-1):
            self.massiv[i] = self.massiv[i - 1]

        self.massiv[index] = value
        self.occupied += 1


    def index(self,value): # Возвращает индекс первого вхождения значения 
        for i in range (0,self.occupied):
            if self.massiv[i] == value:
                return i
          
        raise ValueError("указанного значения индекса в списке нет")
    
    def count(self,value): # Возвращает количество вхождений значения value в векторе
        quantity = 0
        for i in range (0,self.occupied):
            if self.massiv[i]==value:
                quantity+=1
        
        return quantity

    def reverse(self): #Переворачивает порядок элементов на месте
        for i in range(int(self.occupied/2)):
            boofer = self.massiv[i]
            self.massiv[i]= self.massiv[self.occupied-i-1]
            self.massiv[self.occupied - i-1] = boofer


    def sort(self,reverse=True): #Сортирует элементы на месте в порядке возрастания или убывания (если reverse=True)
        for i in range(0,self.occupied):
            for j in range(0,self.occupied-1-i):
                if self.massiv[j]>self.massiv[j+1]:
                    self.massiv[j+1],self.massiv[j] = self.massiv[j],self.massiv[j+1]


    def append(self,element):
        self.increase_memory()

        self.massiv[self.occupied]=element
        self.occupied+=1

    def copy(self):
        new = Vector()
        for i in range(self.occupied):
            new.append(self.massiv[i])
        
        return new
    
    def extend(self,object):
        for el in object:
            self.append(el)



a1 = Vector()   
for i in range(0, 10):
    a1.append(i)  
print("Исходный вектор:", a1)
