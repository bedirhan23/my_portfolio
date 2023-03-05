from xlrd import open_workbook
from recommandations import *
import dbm
import pickle as pk
from tkinter import *
from tkinter import messagebox



class FetchData(object):

    def __init__(self, critics):
        
        self.excel_file='Degerlendirmeler.xls'
        self.meals = self.fetch_dataset(critics)
        
        self.counter=1

    def fetch_dataset(self, critics):
        """Fetches all the dataset from an excel file and returns a list of all
           meals
        """
        book = open_workbook(self.excel_file)
        sheet = book.sheet_by_index(0)
        # Parse the sheet and populate critics dataset
        # by skipping first row.
        for row in range(1, sheet.nrows):
            user = sheet.cell(row, 0).value
            product = sheet.cell(row, 1).value
            rating = float(sheet.cell(row, 2).value)
            critics.setdefault(user, {})
            critics[user][product] = rating

        products=[sheet.cell(row_index,col_index).value for row_index in range(sheet.nrows)\
               for col_index in range(sheet.ncols) if col_index == 1]

        return products[1:]  # omit the meal header



class Recommender():
    def __init__(self, new_master):
        new_master.title("Oneri Sistemi")
        self.new_master=new_master
        self.chosen_meals=[]
        self.critics_dataset={}
        self.method = "userbased"
        self.similarity="euclidean"
        self.sim_dict={"euclidean":sim_distance, "pearson":sim_pearson, "jaccard":sim_jaccard}
        self.current_user="Own"  # current user selected, not in critics_dataset


        try:
            self.veri_sinifi = FetchData(self.critics_dataset)
        except:
            messagebox.showerror(title="Hata",message="Degerlendirmeler dosyasi duzgun yuklenemiyor!!!!")


        # top level labels definitions
        frame1 = Frame(new_master)
        frame1.pack()
        top_label_text="Musteri Urun Oneri Sistemi Ekrani"
        top_label = Label(frame1, text=top_label_text, width=30, font="Times 18 bold")
        top_label.pack()

        # rate a meal labels
        frame2 = Frame(new_master)
        frame2.pack(anchor=W)
        meal_label = Label(frame2, text="Bir yemek secin:")
        meal_label.pack(side=LEFT, anchor=NW, padx=30)
        rate_label = Label(frame2, text="Degerlendirmeniz:")
        rate_label.pack(side=LEFT, anchor=NW, padx=60)

        # Rate a meal widgets.
        frame4 = Frame(new_master)
        frame4.pack(anchor=W)
        self.box_value=StringVar()
        self.box=Listbox(frame4, width=30)
        self.box.pack(side=LEFT, anchor=W, padx=30)
        meal_set  = set(self.veri_sinifi.meals)
        for meal in meal_set:
            self.box.insert(END, meal)

        # entry widget
        self.entry= Entry(frame4, width=10)
        self.entry.pack(side=LEFT)

        # Ekle button
        add = Button(frame4, text="Ekle", width=8, command=self.get_user_ratings)
        add.pack(side=LEFT, padx=20)

        # user rating list box
        self.choice_box=Listbox(frame4, height=6, width=60)
        self.choice_box.pack(side=LEFT, padx=20)



        # Horizontal line.
        frame5 = Frame(new_master)
        frame5.pack()

        # Settings labels
        gar_label = Label(frame5, text="Ayarlar",width=30, font="Times 18 bold")
        gar_label.pack()

        # Settings widgets
        frame6 = Frame(new_master)
        frame6.pack(anchor=W)
        choose_num_ratings=Label(frame6, text="Toplam Oneri Adedi:")
        choose_num_ratings.pack(side=LEFT, padx=22, anchor=N)
        self.num_recommendations= Entry(frame6, width=5)
        self.num_recommendations.pack(side=LEFT, anchor = N)
        self.num_recommendations.insert(END,"3")  # default value

        # Settings widgets
        frame7 = Frame(frame6)
        frame7.pack(side=LEFT)
        settings_label= Label(frame7, text="Oneri Modeli:")
        settings_label.pack(padx=250)

        # set up our radio buttons
        self.v=IntVar()
        self.v.set(1)
        user_based=Radiobutton(frame7, text='Kullanici Bazli',variable=self.v,value=1,
                                  command=self.user_based_sim)
        user_based.pack(anchor=W, padx=250)
        item_based=Radiobutton(frame7, text='Urun Bazli',variable=self.v,value=2,
                                  command=self.item_based_sim)
        item_based.pack(anchor=W, padx=250)

        # similarity widgets
        sim_label = Label(frame7, text="Benzerlik Olcutu:")
        sim_label.pack()

        # similarity radio buttons
        self.v2=IntVar()
        self.v2.set(1)
        euclidean=Radiobutton(frame7,text='Euclidean',variable=self.v2,value=1,
                                 command=self.euclidean_method)
        euclidean.pack()
        pearson=Radiobutton(frame7,text='Pearson',variable=self.v2,value=2,
                               command=self.pearson_method)
        pearson.pack()
        jaccard=Radiobutton(frame7,text='Jaccard',variable=self.v2,value=3,
                               command=self.jaccard_method)
        jaccard.pack()

        # Horizontal line.
        frame8 = Frame(new_master)
        frame8.pack(anchor=W)

        # Get Recommendations
        frame9 = Frame(new_master)
        frame9.pack(anchor=W)
        get_rec=Button(frame9, text="Oneri Al",
                              command=self.get_recommendations)
        get_rec.pack(side=LEFT, padx=155,pady=10)

        get_sim=Button(frame9, text="Benzer Musterileri Listele", 
                              command=self.populate_simuser_box)
        get_sim.pack(side=LEFT,padx=230,pady=10)

        # Result boxes
        frame10 =Frame(new_master)
        frame10.pack(anchor=W)
        frame11 = Frame(frame10)
        frame11.pack(side=LEFT, padx=10)

        self.result_box = Text(frame11,width=45, height=7)
        self.result_box.pack(side=LEFT)

        frame12 = Frame(frame10)
        frame12.pack(side=LEFT, padx=75)
        self.simuser_box=Text(frame12, height=7, width=45)
        self.simuser_box.pack(side=LEFT)

        self.open_previous_ratings()

    def open_previous_ratings(self):
        """opens any previous ratings that the user made"""
        db = dbm.open("ownratings2", "c")
        try:
            ratings=pk.loads(db[self.current_user])
            print("Kullanici ile ilgili veri bulundu", self.current_user)
            print(ratings)
            for meal, rating in ratings.items():
                meal_index=self.veri_sinifi.meals.index(meal)
                self.chosen_meals.append(meal_index)
                self.choice_box.insert(END, "%s --> %s"%(meal, rating))
                self.critics_dataset.setdefault(self.current_user, {})
                self.critics_dataset[self.current_user][meal] = rating
        except KeyError:
            print("Kullanici daha once veri girmemis", self.current_user)
            db[self.current_user]=pk.dumps({})
            self.critics_dataset.setdefault(self.current_user, {})

        db.close()

    def get_user_ratings(self):
        
        if self.box.curselection() == ():
            messagebox.showerror(title="Hata",message="Degerlendirme puani girebilmek icin en az bir yemek secili olmali!")
            return
        selected_meal=self.box.get(self.box.curselection())
        self.chosen_meals.append(self.box_value.get())
        meal_rating = float(self.entry.get())
        db=dbm.open("ownratings2","c")
        db_keys = [db_key.decode("UTF-8") for db_key in db.keys()]
        if self.current_user in db_keys:
            user_ratings = pk.loads(db[str(self.current_user)])
            user_ratings[str(selected_meal)]= meal_rating
            db[str(self.current_user)]=pk.dumps(user_ratings)
        else:
            user_ratings=dict()
            user_ratings[str(selected_meal)]=meal_rating
            db[str(self.current_user)]=pk.dumps(user_ratings)

        self.critics_dataset.setdefault(self.current_user, {})
        self.critics_dataset[self.current_user][selected_meal] = meal_rating
        self.choice_box.insert(END, "%s --> %s"%(selected_meal, meal_rating))



    def get_recommendations(self):
        """This method is the command for the get standard recommendations button widget in the
           application. It uses the database to create a dictionary that will be used to feed into the
           get_recommendations function"""
        self.clear_result_box()
        if self.method == "userbased":
            sim_func=self.sim_dict[self.similarity]
            if self.current_user not in self.critics_dataset:
                self.result_box.insert(END, "Lutfen bir kac yemek degerlendirin")
                return
            recommendations=getRecommendations(self.critics_dataset, self.current_user, sim_func)
            num_of_rec=self.num_recommendations
            self.result_box.insert(END, "Skor --> Oneri\n")
            loop_range=int(num_of_rec.get())
            if loop_range>len(recommendations):
                loop_range=len(recommendations)
            if loop_range==0:
                self.result_box.insert(END,"Oneri Bulunamadi, daha cok yemek degerlendirin.")
            for i in range(loop_range):
                sim_score=recommendations[i][0]  # similarity score
                rec=recommendations[i][1]  # recommended meal
                self.result_box.insert(END, "%.2f --> %s\n"%(sim_score, rec))
        else:
            if self.current_user not in self.critics_dataset:
                self.result_box.insert(END, "Lutfen bir kac yemek degerlendirin")
                return
            num_of_rec=self.num_recommendations
            loop_range=int(num_of_rec.get())
            similar_items=calculateSimilarItems(self.critics_dataset)
            recommendations=getRecommendedItems(self.critics_dataset, similar_items, self.current_user)
            self.result_box.insert(END, "Skor --> Oneri\n")
            if loop_range>len(recommendations):
                loop_range=len(recommendations)
            if loop_range==0:
                self.result_box.insert(END,"Oneri Bulunamadi, daha cok yemek degerlendirin.")
            for i in range(loop_range):
                sim_score=recommendations[i][0]  # similarity score
                rec=recommendations[i][1]  # recommended meal
                self.result_box.insert(END, "%.2f --> %s\n"%(sim_score, rec))


    def populate_simuser_box(self):
        """This method populates the similar users listbox"""
        self.clear_simuser_box()
        sim_func=self.sim_dict[self.similarity]
        top=topMatches(self.critics_dataset,self.current_user,5,sim_func)
        self.simuser_box.insert(END, "Benzerlik --> Kisi\n")
        for score, person in top:
            self.simuser_box.insert(END, "%.2f  -->   %s\n" % (score, person))


    def clear_result_box(self):
        # clears everything that is in the result box
        self.result_box.delete("1.0","end-1c")

    def clear_simuser_box(self):
        self.simuser_box.delete("1.0", "end-1c")

    # the following 5 methods are made as commands for radio buttons
    def euclidean_method(self):
        self.similarity="euclidean"

    def pearson_method(self):
        self.similarity="pearson"

    def jaccard_method(self):
        self.similarity="jaccard"

    def user_based_sim(self):
        self.method="userbased"

    def item_based_sim(self):
        self.method="itembased"


if __name__ == "__main__":
    root = Tk()
    Recommender(root)
    root.mainloop()