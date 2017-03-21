# -*-conding:utf8-*-
# /usr/bin/python3
import pymongo

text_1 = """在自由城建立后的最初的十年间，所有的毒品在这里都被允许使用和交易。这也造成了极其严重的后果。仅仅在 1978 和 1979 年这两年，就有 10 人因为吸食毒品过量死在了自由城。自由城的居民们再也无法忍受这种毒品泛滥的情况，在尝试与丹麦警察合作失败后，自由城中所有的居民，无论男女老幼，纷纷走上街头，对自由城进行了 40 天的昼夜不断的巡逻，每当遇见毒贩子，就对他们发出最后的通牒：放弃毒品或者离开自由城。最终，毒贩子们被武力驱赶出了自由城，也有超过 60 名瘾君子被送进了戒毒所。这是 Christiania 历史上著名的“Junk Blockade”事件。至此，自由城开始禁止一切“hard drug”的使用与交易。 “Junk Blockade”期间，自由城居民们在城中竖起了“Junk is death”的牌子 虽然 hard drug 被驱赶出了自由城。但是 40 多年来，以大麻为代表的软性毒品在自由城中一直受到保护和追捧。自由城中的大麻交易集中在城中的 Pusher Street. 下图街道两边的亭子里就是大麻的销售场所。 在 Pusher Street 有三条规定：“have fun”、“No photo”和“Do not run”。
曾在自由城的一处自制建筑上看到这样一段话（T.E.Lawrence 的名言）：All men dream: but not equally. Those who dream by night in the dusty recesses of their minds wake in the day to find that it was vanity: but the dreamers of the day are dangerous men, for they may act their dreams with open eyes, to make it possible.
自由城的居民喜爱艺术，单单是音乐厅，在自由城内就有好几个，有室内的也有露天的。其中最著名的当属 Grey hall， 这座音乐厅始建于 1891 年，可容纳数千人。与自由城内的居民聊天，他们自豪的告诉我：鲍勃迪伦、绿日乐队、blur 等等知名的乐队和歌手都曾经在自由城表演过。现在，每周依然会有来自世界各地的艺术家在自由城内的各个音乐厅表演。
也许自由城的居民们都是白日梦想家，他们活在乌托邦的幻想里，但同时他们好像又成了实干家，他们竟把这幻想变为了现世，他们真的创造出了一个乌托邦。"""
text_2 = "曾有人在一处自制建筑上看到这样一段话: All men dream: but not equally. Those who dream by night in the dusty recesses of their minds wake in the day to find that it was vanity: but the dreamers of the day are dangerous men, for they may act their dreams with open eyes, to make it possible.也许自由城的居民们都是白日梦想家，他们活在乌托邦的幻想里，但同时他们好像又成了实干家，他们竟把这幻想变为了现世，他们真的创造出了一个乌托邦。"
