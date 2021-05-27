from extractor import GoogleImageExtractor

bot = GoogleImageExtractor("Rakul", 10, "./Rakul Images", False)
bot.apply_safesearch(False)
bot.apply_search_filters(color="red")
bot.run()