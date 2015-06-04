from page import Page

class Paginator(object):
    page_per_count = 5 

    def __init__(self, pagePerCount=5):
        self.page_per_count; 

    def get_total_page_count(self, total_count):
        m, n = divmod(total_count, self.page_per_count)        
        total_page_count = m

        
        if n !=0:
            total_page_count+=1  
        return total_page_count



    def get_page_list(self, current_page, total_page_count):
        page_list = list()
        for i in range(1, total_page_count+1):
            active = False
            if i == current_page:
                active = True 
            
            page_list.append(Page(i, active))
        return page_list
 

    def paging(self, current_page, total_count): 
        
        total_page_count = self.get_total_page_count(total_count)
        page_list = self.get_page_list(current_page, total_page_count)

        #
        prev_end_index = (current_page-1) * self.page_per_count
        current_end_index = current_page * self.page_per_count 


        return prev_end_index, current_end_index, page_list