import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont


class App(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        style = ttk.Style()
        style.theme_use("alt")  # this line is important in order to add background color in the heading section

        style.configure("My.Treeview.Heading",
                        background='green',
                        foreground='white')

        style.map('My.Treeview.Heading',
                  background=[('active', 'red')])  # this line for hovering over the heading section

        # Create the main container frame
        container = ttk.Frame(parent)
        container.grid(row=0, column=0, sticky='nsew')

        # Set initial size of the container frame (adjust as needed)
        container.grid_propagate(False)  # Prevent container from resizing
        container.config(width=800, height=500)  # Set width and height of container frame

        # Create Treeview with columns
        self.tree = ttk.Treeview(container, style="My.Treeview",columns=("size", "modified"))
        self.tree["columns"] = ("date", "time", "loc")

        self.tree.column("#0", width=100, anchor='center')
        self.tree.column("date", width=100, anchor='center')
        self.tree.column("time", width=100, anchor='center')
        self.tree.column("loc", width=100, anchor='center')

        self.tree.heading("#0", text="Name")
        self.tree.heading("date", text="Date")
        self.tree.heading("time", text="Time")
        self.tree.heading("loc", text="Location")

        # Insert items into the Treeview

        for _ in range(10):  # Add more items to demonstrate scrolling
            self.tree.insert("", "end", text="Grace", values=("2010-09-23", "03:44:53", "Garden"))
        for _ in range(10):  # Add more items to demonstrate scrolling
            self.tree.insert("", "end", text="John", values=("2017-02-05", "11:30:23", "Airport"))
        for _ in range(10):  # Add more items to demonstrate scrolling
            self.tree.insert("", "end", text="Betty", values=("2014-06-25", "18:00:00", ""))
        for _ in range(10):  # Add more items to demonstrate scrolling
            self.tree.insert("", "end", text="Eddie", values=("2014-06-19", "15:00:00", "Bus station"))
        for _ in range(10):  # Add more items to demonstrate scrolling
            self.tree.insert("", "end", text="hello", values=("2014-06-19", "15:00:00", "Train"))
        for _ in range(10):  # Add more items to demonstrate scrolling
            self.tree.insert("", "end", text="world", values=("2014-06-19", "15:00:00", "Cargo"))

        # Create vertical and horizontal scrollbars
        vsb = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(container, orient="horizontal", command=self.tree.xview)

        # Configure the treeview to use the scrollbars
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Arrange treeview and scrollbars in the grid
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        # Make the container expandable
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Bind scroll events to update the canvas position
        self.tree.bind('<ButtonRelease-1>', self.selectItem)
        self.tree.bind('<Configure>', self.updateCanvasPosition)
        self.tree.bind('<Motion>', self.updateCanvasPosition)
        self.tree.bind('<MouseWheel>', self.updateCanvasPosition)
        self.tree.bind('<Button-4>', self.updateCanvasPosition)  # Linux scroll up
        self.tree.bind('<Button-5>', self.updateCanvasPosition)  # Linux scroll down
        self.tree.bind('<Shift-MouseWheel>', self.updateCanvasPosition)
        self.tree.bind('<ButtonPress-1>', self.updateCanvasPosition)
        self.tree.bind('<<TreeviewSelect>>', self.updateCanvasPosition)

        # Create a Canvas Overlay to show selected Treeview cell
        sel_bg = 'red'
        sel_fg = 'black'
        self.setup_selection(sel_bg, sel_fg)

        self.selected_iid = None
        self.selected_column = None

    def setup_selection(self, sel_bg, sel_fg):
        self._font = tkFont.Font()

        self._canvas = tk.Canvas(self.tree, background=sel_bg, borderwidth=1, highlightthickness=1)
        self._canvas.text = self._canvas.create_text(0, 0, fill=sel_fg, anchor='w')

    def selectItem(self, event):
        # Remove Canvas overlay from GUI
        self._canvas.place_forget()

        # Local Parameters
        x, y, widget = event.x, event.y, event.widget
        iid = widget.identify_row(y)
        column = event.widget.identify_column(x)
        item = widget.item(iid)
        itemText = item['text']
        itemValues = item['values']
        print(item)

        # Leave method if mouse pointer clicks on Treeview area without data
        if not column or not iid:
            return

        # Leave method if selected item's value is empty
        if not len(itemValues):
            return

        # Get value of selected Treeview cell
        if column == '#0':
            self.cell_value = itemText
        else:
            self.cell_value = itemValues[int(column[1]) - 1]

        # Leave method if selected Treeview cell is empty
        if not self.cell_value:
            return

        # Store selected item and column for updating the canvas position
        self.selected_iid = iid
        self.selected_column = column

        # Get the bounding box of selected cell
        bbox = widget.bbox(iid, column)
        print(bbox,iid,column)
        if not bbox:
            return

        # Update and show selection in Canvas Overlay
        self.show_selection(widget, bbox, column)

    def show_selection(self, parent, bbox, column):
        """Configure canvas and canvas-textbox for a new selection."""
        x, y, width, height = bbox
        fudgeTreeColumnx = 19  # Determined by trial & error
        fudgeColumnx = 15  # Determined by trial & error

        # Number of pixels of cell value in horizontal direction
        textw = self._font.measure(self.cell_value)

        # Make Canvas size to fit selected cell
        self._canvas.configure(width=width, height=height)

        # Position canvas-textbox in Canvas
        if column == '#0':
            self._canvas.coords(self._canvas.text, fudgeTreeColumnx, height / 2)
        else:
            self._canvas.coords(self._canvas.text, (width - (textw - fudgeColumnx)) / 2.0, height / 2)

        # Update value of canvas-textbox with the value of the selected cell.
        self._canvas.itemconfigure(self._canvas.text, text=self.cell_value)

        # Overlay Canvas over Treeview cell
        self._canvas.place(in_=parent, x=x, y=y)

    def updateCanvasPosition(self, event=None):
        """Update the canvas position when the treeview is scrolled."""
        if self.selected_iid and self.selected_column:
            bbox = self.tree.bbox(self.selected_iid, self.selected_column)
            if bbox:
                self.show_selection(self.tree, bbox, self.selected_column)
            else:
                self._canvas.place_forget()  # Hide the canvas if the item is not visible

if __name__ == "__main__":
    window = tk.Tk()
    app = App(window)
    window.mainloop()
