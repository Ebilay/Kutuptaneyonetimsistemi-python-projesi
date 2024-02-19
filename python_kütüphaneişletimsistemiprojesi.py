class Library:
    def __init__(self):
        self.kitap_dosyaadi = "books.txt"
        self.ödüncalma_dosyaadi = "borrowed_books.txt"
        self.initialize_files()

    def initialize_files(self):
        # Kitap dosyasını oluştur veya varsa içeriğini kontrol et
        with open(self.kitap_dosyaadi, "a+") as kitap_dosyasi:
            kitap_dosyasi.seek(0)
            if not kitap_dosyasi.read(1):
                kitap_dosyasi.write("")

        # Ödünç alınan kitap dosyasını oluştur veya varsa içeriğini kontrol et
        with open(self.ödüncalma_dosyaadi, "a+") as ödüncalma_dosyasi:
            ödüncalma_dosyasi.seek(0)
            if not ödüncalma_dosyasi.read(1):
                ödüncalma_dosyasi.write("")

    def list_books(self):
        """Kütüphanedeki tüm kitapları listeler."""
        with open(self.kitap_dosyaadi, "r") as file:
            for line in file:
                book_title, author, status, *_ = line.strip().split(",")
                is_copy = "(Kopya)" if "(Kopya)" in book_title else ""
                if status == "Kütüphane":
                    print(f"{author} - {book_title.replace('(Kopya)', '')} {is_copy}")
                elif status == "Ödünç":
                    print(f"{author} - {book_title} {is_copy} (Ödünç Alındı)")

    def add_book(self):
        """Kütüphaneye yeni bir kitap ekler."""
        book_title = input("Kitap Adı: ")
        author = input("Yazar Adı: ")
        release_year = input("Yayın Yılı: ")
        num_pages = input("Sayfa Sayısı: ")
        copy = input("Bu bir kopya mı? (Evet/Hayır): ").lower()

        if copy == "evet":
            copy_number = input("Kaçıncı kopya olduğunu belirtiniz: ")
            book_title += f" ({copy_number})"

        with open(self.kitap_dosyaadi, "a") as file:
            file.write(f"{book_title},{author},Kütüphane,{release_year},{num_pages}\n")
        print(f"{author} tarafından yazılan {book_title} kitabı başarıyla listeye eklendi.")

    def borrow_book(self):
        """Kütüphaneden kitap ödünç alır."""
        from datetime import datetime, timedelta
        book_title = input("Ödünç almak istediğiniz kitabın adını girin\n(Aynı kitaplar için parantez ile birlikte kopya sayısınıda yazınız): ")
        borrower_name = input("Ödünç alan kişinin adı ve soyadı: ")
        borrowing_date = datetime.now().strftime("%Y-%m-%d")
        due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

        # Kitabın mevcut olup olmadığını kontrol et
        found = False
        with open(self.kitap_dosyaadi, "r") as file:
            lines = file.readlines()

        with open(self.kitap_dosyaadi, "w") as file:
            for line in lines:
                saved_book_title, author, status, *_ = line.strip().split(",")
                if book_title == saved_book_title:
                    if status == "Ödünç":
                        print(f"{book_title} kitabı zaten ödünç alınmış.")
                        return
                    else:
                        file.write(f"{saved_book_title},{author},Ödünç,{borrowing_date}\n")
                        found = True
                else:
                    file.write(line)
        
        if not found:
            print(f"{book_title} kitabı kütüphanede mevcut değil.")
            return

        # Ödünç alınan kitabı kaydet
        with open(self.ödüncalma_dosyaadi, "a") as file:
            file.write(f"{book_title},{borrowing_date},{due_date},{borrower_name}\n")
        print(f"{book_title} kitabını {borrower_name} isimli kişi ödünç aldı.")
        print(f"Lütfen {due_date} tarihine kadar {book_title} kitabını iade ediniz.")
    
    def remove_book(self):
        """Kütüphaneden bir kitabı kaldırır."""
        book_title = input("Silmek istediğiniz kitabın adını girin(Aynı olan kitaplar için parantez ile birlikte içindeki kopya sayısını belirtelerek yazınız): ")
        author = input("Yazarın adını girin: ")

        with open(self.kitap_dosyaadi, "r") as file:
            lines = file.readlines()

        removed = False
        with open(self.kitap_dosyaadi, "w") as file:
            for line in lines:
                saved_book_title, saved_author, *_ = line.strip().split(",")
                if book_title == saved_book_title and author == saved_author and not removed:
                    removed = True
                else:
                    file.write(line)

        if removed:
            print("Kitap başarıyla silindi.")
        else:
            print(f"{book_title} kitabı {author} tarafından yazılanlar arasında bulunamadı veya kitap zaten silinmiş olabilir.")

    def __del__(self):
        print("Vakit ayırdığınız için teşekkür ederiz. Unutmayın, her kitap yeni bir maceradır! Okumaya doyamadığınız anlarda tekrar bekleriz...")

def main():
    library = Library()

    while True:
        print("*** MENU ***")
        print("1) Kitapları Listele")
        print("2) Kitap Ekle")
        print("3) Kitap Ödünç Al")
        print("4) Kitap Sil")
        print("5) Çıkış")
        choice = input("Lütfen yapmak istediğiniz işlem için 1 ila 4 arasında bir seçim yapınız \nÇıkış yapmak için 5 veya q tuşlarını kullanabilirsiniz: ")

        if choice == "1":
            library.list_books()
            input("Ana menüye dönmek için Enter tuşuna basın.")
        elif choice == "2":
            library.add_book()
            input("Ana menüye dönmek için Enter tuşuna basın.")
        elif choice == "3":
            library.borrow_book()
            input("Ana menüye dönmek için Enter tuşuna basın.")
        elif choice == "4":
            library.remove_book()
            input("Ana menüye dönmek için Enter tuşuna basın.")
        elif choice.lower() == "q" or choice == "5":
            print("Programdan çıkılıyor...")
            break
        else:
            print("Geçersiz seçim. Lütfen tekrar deneyin.")

if __name__ == "__main__":
    main()
