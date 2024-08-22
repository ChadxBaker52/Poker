import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from deck_of_cards import Deck, Hand, Balance
    
class BlackjackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")
        
        self.deck = Deck(6)
        self.player_hand = Hand()
        self.dealer_hand = Hand(flipped=True)
        
        self.player_balance = Balance()
        
        self.card_images = {}  # Store images to prevent garbage collection
        
        self.create_widgets()
        self.new_game()
        
    def create_widgets(self):
        self.dealer_frame = tk.Frame(self.root)
        self.dealer_frame.pack(pady=10)
        
        self.player_frame = tk.Frame(self.root)
        self.player_frame.pack(pady=10)
        
        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(pady=20)
        
        self.hit_button = tk.Button(self.controls_frame, text="Hit", command=self.hit)
        self.hit_button.pack(side="left", padx=10)
        
        self.stand_button = tk.Button(self.controls_frame, text="Stand", command=self.stand)
        self.stand_button.pack(side="left", padx=10)
        
        self.new_game_button = tk.Button(self.controls_frame, text="New Game", command=self.new_game)
        self.new_game_button.pack(side="left", padx=10)
        
    def new_game(self):
        self.deck.shuffle()
        self.player_hand = Hand()
        self.dealer_hand = Hand(flipped=True)
        
        self.player_hand.get_card(self.deck)
        self.dealer_hand.get_card(self.deck)
        self.player_hand.get_card(self.deck)
        self.dealer_hand.get_card(self.deck)
        
        self.update_display()
        
    def update_display(self):
        for widget in self.player_frame.winfo_children():
            widget.destroy()
            
        for widget in self.dealer_frame.winfo_children():
            widget.destroy()
            
        tk.Label(self.dealer_frame, text="Dealer's Hand:").pack()
        for card in self.dealer_hand.cards:
            if self.dealer_hand.flipped and self.dealer_hand.cards.index(card) == 1:
                image_path = "cards/card_back_red.png"
            else:
                image_path = card.get_image_path()
                
            if image_path not in self.card_images:
                image = Image.open(image_path)
                resized_image = image.resize((150, 200))  # Resize to 100x150 pixels
                tk_image = ImageTk.PhotoImage(resized_image)
                self.card_images[image_path] = tk_image
            label = tk.Label(self.dealer_frame, image=self.card_images[image_path])
            label.pack(side="left")
        
        if self.dealer_hand.flipped:
            tk.Label(self.dealer_frame, text=f"Value: ?").pack()
        else:
            tk.Label(self.dealer_frame, text=f"Value: {self.dealer_hand.get_value()}").pack()
        
        tk.Label(self.player_frame, text="Player's Hand:").pack()
        for card in self.player_hand.cards:
            image_path = card.get_image_path()
            if image_path not in self.card_images:
                image = Image.open(image_path)
                resized_image = image.resize((150, 200))  # Resize to 100x150 pixels
                tk_image = ImageTk.PhotoImage(resized_image)
                self.card_images[image_path] = tk_image
            label = tk.Label(self.player_frame, image=self.card_images[image_path])
            label.pack(side="left")
        tk.Label(self.player_frame, text=f"Value: {self.player_hand.get_value()}").pack()
        
    def hit(self):
        self.player_hand.get_card(self.deck)
        self.update_display()
        if self.player_hand.get_value() > 21:
            messagebox.showinfo("Blackjack", "Player busts! Dealer wins.")
            self.new_game()
        
    def stand(self):
        self.dealer_hand.flipped = False
        self.root.after(1500, self.dealer_turn)
        self.update_display()

    def dealer_turn(self):
        if self.dealer_hand.get_value() < 17:
            self.dealer_hand.get_card(self.deck)
            self.update_display()
            self.root.after(1500, self.dealer_turn)
        else:
            self.finish_game()

    def finish_game(self):
        self.update_display()
        
        player_value = self.player_hand.get_value()
        dealer_value = self.dealer_hand.get_value()
        
        if dealer_value > 21 or player_value > dealer_value:
            messagebox.showinfo("Blackjack", "Player wins!")
        elif player_value < dealer_value:
            messagebox.showinfo("Blackjack", "Dealer wins!")
        else:
            messagebox.showinfo("Blackjack", "It's a tie!")
        self.new_game()

root = tk.Tk()
app = BlackjackGUI(root)
root.mainloop()