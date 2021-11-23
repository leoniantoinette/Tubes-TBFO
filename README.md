# Tugas Besar IF2124 Teori Bahasa Formal dan Otomata
## Compiler Bahasa Python
Kelompok Sabeb
1. Fikra Hadi Ramadhan (13518036) 
2. Christine Hutabarat (13520005) 
3. Flavia Beatrix Leoni A. S. (13520051) 

### Deskripsi
Program dapat digunakan untuk mengevaluasi kebenaran syntax dari masukan berupa kode dalam bahasa Python dengan menggunakan konsep CFG DAN FA.

### Cara Menggunakan:
Program dapat menerima input berupa suatu teks file atau string yang merupakan kode dari sebuah program.  
Apabila input berupa file eksternal, jalankan command ini pada terminal  
```
py main.py <input_file.txt>
```  
contoh:  
```
py main.py input.txt
```
Apabila input berupa string, jalankan command ini pada terminal    
```
py main.py "string"
```  
contoh:  
```
py main.py "print(2+3)"
```
Program akan menampilkan "Accepted!" jika input diterima atau "Syntax Error!" jika input tidak diterima.  