SAVE_DATA_INTO_SRF = """
/*Insert Data in srf (SRF Save); */

INSERT INTO dbo.srf(style, style_pid, sample_pid,season, factory,color_code,description,project_name,brand,style_size,
saved,request_status,Qty,reqno,send_to_vendor,sample_sent,req_exfactory,RU,size_values,season_id,sell_style,created_date,
updated_date,request_notes,design_cmt,pd_cmt,qa_cmt,brand_cmt,quantity_cmt,[user],updated_time,id)
VALUES ('eapple', 'apple_100_dynamic_S24', 'apple_100_dynamic_S24_L_1','24','dynamic' ,'100','This is my favourite','Favourite fruit',
'DICKI','L',1,0,6,1,0,'07/07/2023','07/06/2023',2,3,'S24','appleL','2023-07-07','07/07/2023',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);


"""

SAVE_DATA_INTO_STATUS = """
INSERT into dbo.status (style, tech_pack_status,total_colors,approved_colors,pending_colors,total_sizes,approved_sizes,
pending_sizes,Design_documents_status,PD_documents_status,QA_documents_status,total_line_items,season,season_id,
sell_style,vendor) VALUES ('eapple','0',0,0,0,0,0,0,'1','1','1',0,'S24','24','eappleL','')
"""

SAVE_DATA_INTO_SRT = """
INSERT into dbo.srt (reqno,sample_pid,style_pid,style,factory,color_code,season,project_name,description,request_date,Qty,
size,brand_status,design_status,pd_status,qa_status,request_recieved,promised_exfactory,pvf_cmt,brand_cmt,design_cmt,
pd_cmt,qa_cmt,brand,QtyRcd,created_date,updated_date,season_id,sell_style,overall_status,SLTD,quantity_cmt,[user],
updated_time,req_exfactory,previous_pd_status,previous_qa_status,previous_design_status,previous_brand_status,
previous_overall_status,droa_needed) VALUES (1,'eaaple_100_dynamic_S24_L_1','eaaple_100_dynamic_S24','eapple','dynamic','100',
'S24','this is my fav fruit','Favourite fruit','','','L',Null,'Approved','Override','Approved','','','','','','','',
'DICKI',7,'','','24','eappleL','','','','','','','','','','','',0);
"""

UPDATE_SRT_PRODUCT_READY_STATUS = """
--Update status in SRT to check the product ready status change:

Update dbo.srt set design_status = 'Approved',pd_status = 'Override',qa_status = 'Approved' where style = 'eapple' 
and color_code = '100';
"""

SELECT_STYLE_FOR_PRODUCT_READY_STATUS = """
--Select the styles having at least one vendor with all the status approved/override and brand status = N/A:

select ROW_NUMBER() OVER (ORDER BY newId()) as id, alll.brand, alll.style, alll.size, alll.factory  from 
(select b_apvd.style, b_apvd.size, count(b_apvd.color_code) as color_count , b_apvd.factory , b_apvd.brand
from (select a_apvd.style, a_apvd.size, a_apvd.factory , a_apvd.color_code , a_apvd.brand
from   (select color_code,style, size , factory, brand, reqno
from dbo.srt where pd_status in ('Approved', 'Override')
and qa_status in ('Approved', 'Override') 
and design_status in ('Approved', 'Override') 
and brand_status in ('N/A') ) as a_apvd  
group by style, size, color_code , factory, brand) as b_apvd group by b_apvd.style, b_apvd.factory, b_apvd.size, b_apvd.brand
) as apvd inner join 
(select  a_all.style, a_all.size, a_all.factory, a_all.brand,max(a_all.color_code) as color_code_count
from (select style, size, count( color_code) as color_code, factory, reqno , brand
from dbo.srt group by style, size, factory, reqno, brand) as a_all group by a_all.style, a_all.size, a_all.factory, a_all.brand)
as alll on apvd.style=alll.style and apvd.factory=alll.factory and apvd.size = alll.size and apvd.color_count = alll.color_code_count;"""

UPDATE_FOR_DAILY_SRT_REPORT = """
----/*'Update received samples(Daily SRT Report)';*/

Update dbo.srt SET request_recieved='07/07/2023' ,QtyRcd=24 where style='eapple';
"""

UPDATE_FOR_DAILY_ROA_REPORT = """
/*'''ROA Update''';*/

update dbo.srt SET brand_status = 'Set_up_Ready',qa_status= 'Override',pd_status = 'Approved',design_status = 'Approved'
where style='eapple';
"""

UPDATE_EXCEPTION_REPORT = """
/*'''Status Update(Exception report)''';*/

update dbo.srt SET brand_status = 'Set_up_Ready',qa_status= 'Override',pd_status = 'Approved',design_status = 'Rejected'
where style='eapple', updated_date='07/09/2023';"""

DELETE_ALL_RECORDS = """
--Delete data from srt and status:

delete from dbo.srt where style = 'eapple';
delete  from dbo.status where style = 'eapple';
delete from dbo.srf where style = 'eapple';
"""

SAVE_DATA_ROA_STATUS = """
INSERT INTO [dbo].[srt]
           ([reqno], [sample_pid], [style_pid], [style], [factory], [color_code], [season], [project_name], [description], [request_date], [Qty], [size], [brand_status], [design_status], [pd_status], [qa_status], [request_recieved], [promised_exfactory], [pvf_cmt], [brand_cmt], [design_cmt], [pd_cmt], [qa_cmt], [brand], [QtyRcd], [created_date], [updated_date], [season_id], [sell_style], [overall_status], [SLTD], [quantity_cmt], [user], [updated_time], [req_exfactory], [previous_pd_status], [previous_qa_status], [previous_design_status], [previous_brand_status], [previous_overall_status], [droa_needed])
     VALUES
           ('1', 'eapple_100_dynamic_S24_L_1', 'eapple_100_dynamic_S24', 'eapple', 'dynamic', '100', '24', 'Favourite_fruit', 'This_is_my_favourite', '{}', '6', 'L', 'Set_up_Ready', 'Approved', 'Approved', 'Approved', NULL, NULL, '', '', '', '', '', 'DICKI', NULL, '{}', '{}', 'S24', 'eappleL', '0', NULL, NULL, NULL, '15:54:01', '07/23/2023', NULL, NULL, NULL, NULL, NULL, '0')

INSERT INTO [dbo].[srt]
           ([reqno], [sample_pid], [style_pid], [style], [factory], [color_code], [season], [project_name], [description], [request_date], [Qty], [size], [brand_status], [design_status], [pd_status], [qa_status], [request_recieved], [promised_exfactory], [pvf_cmt], [brand_cmt], [design_cmt], [pd_cmt], [qa_cmt], [brand], [QtyRcd], [created_date], [updated_date], [season_id], [sell_style], [overall_status], [SLTD], [quantity_cmt], [user], [updated_time], [req_exfactory], [previous_pd_status], [previous_qa_status], [previous_design_status], [previous_brand_status], [previous_overall_status], [droa_needed])
     VALUES
           ('1', 'eapple_101_walt_S24_L_1', 'eapple_101_walt_S24', 'eapple', 'walt', '101', '24', 'Favourite_fruit', 'This_is_my_favourite', '{}', '6', 'L', 'Set_up_Ready', 'Approved', 'Approved', 'Approved', NULL, NULL, '', '', '', '', '', 'DICKI', NULL, '{}', '{}', 'S24', 'eappleL', '0', NULL, NULL, NULL, '15:54:01', '07/23/2023', NULL, NULL, NULL, NULL, NULL, '0')
           
INSERT INTO [dbo].[srt]
           ([reqno], [sample_pid], [style_pid], [style], [factory], [color_code], [season], [project_name], [description], [request_date], [Qty], [size], [brand_status], [design_status], [pd_status], [qa_status], [request_recieved], [promised_exfactory], [pvf_cmt], [brand_cmt], [design_cmt], [pd_cmt], [qa_cmt], [brand], [QtyRcd], [created_date], [updated_date], [season_id], [sell_style], [overall_status], [SLTD], [quantity_cmt], [user], [updated_time], [req_exfactory], [previous_pd_status], [previous_qa_status], [previous_design_status], [previous_brand_status], [previous_overall_status], [droa_needed])
     VALUES
           ('1', 'eapple_100_walt_S24_S_1', 'eapple_100_walt_S24', 'eapple', 'walt', '100', '24', 'Favourite_fruit', 'This_is_my_favourite', '{}', '6', 'S', 'Set_up_Ready', 'Approved', 'Approved', 'Approved', NULL, NULL, '', '', '', '', '', 'DICKI', NULL, '{}', '{}', 'S24', 'eappleS', '0', NULL, NULL, NULL, '15:54:01', '07/23/2023', NULL, NULL, NULL, NULL, NULL, '0')

           """

SAVE_DATA_DROA_STATUS = """
INSERT INTO [dbo].[srt]
           ([reqno], [sample_pid], [style_pid], [style], [factory], [color_code], [season], [project_name], [description], [request_date], [Qty], [size], [brand_status], [design_status], [pd_status], [qa_status], [request_recieved], [promised_exfactory], [pvf_cmt], [brand_cmt], [design_cmt], [pd_cmt], [qa_cmt], [brand], [QtyRcd], [created_date], [updated_date], [season_id], [sell_style], [overall_status], [SLTD], [quantity_cmt], [user], [updated_time], [req_exfactory], [previous_pd_status], [previous_qa_status], [previous_design_status], [previous_brand_status], [previous_overall_status], [droa_needed])
     VALUES
           ('1', 'apple_100_dynamic_S24_L_1', 'apple_100_dynamic_S24', 'eapple', 'dynamic', '100', '24', 'Favourite_fruit', 'This_is_my_favourite', '{}', '6', 'L', 'Set_up_Ready', 'Approved', 'Approved', 'Approved', '{}', NULL, '', '', '', '', '', 'DICKI', '2', '{}', '{}', 'S24', 'eappleL', '0', NULL, NULL, NULL, '15:54:01', '{}', NULL, NULL, NULL, NULL, NULL, '0')
"""

SAVE_DATA_DAILY_STATUS_REPORT_SAVE = """
INSERT INTO [dbo].[srt]
           ([reqno], [sample_pid], [style_pid], [style], [factory], [color_code], [season], [project_name], [description], [request_date], [Qty], [size], [brand_status], [design_status], [pd_status], [qa_status], [request_recieved], [promised_exfactory], [pvf_cmt], [brand_cmt], [design_cmt], [pd_cmt], [qa_cmt], [brand], [QtyRcd], [created_date], [updated_date], [season_id], [sell_style], [overall_status], [SLTD], [quantity_cmt], [user], [updated_time], [req_exfactory], [previous_pd_status], [previous_qa_status], [previous_design_status], [previous_brand_status], [previous_overall_status], [droa_needed])
     VALUES
           ('1', 'apple_100_dynamic_S24_L_1', 'apple_100_dynamic_S24', 'eapple', 'dynamic', '100', '24', 'Favourite_fruit', 'This_is_my_favourite', '{}', '6', 'L', 'Set_up_Ready', 'Approved', 'Approved', 'Rejected', '{}', NULL, '', '', '', '', '', 'DICKI', '2', '{}', '{}', 'S24', 'eappleL', '0', NULL, NULL, NULL, '15:54:01', '{}', NULL, NULL, NULL, NULL, NULL, '0')
"""

SAVE_DATA_DAILY_REPORT_SAVE = """
INSERT INTO [dbo].[srt]
           ([reqno], [sample_pid], [style_pid], [style], [factory], [color_code], [season], [project_name], [description], [request_date], [Qty], [size], [brand_status], [design_status], [pd_status], [qa_status], [request_recieved], [promised_exfactory], [pvf_cmt], [brand_cmt], [design_cmt], [pd_cmt], [qa_cmt], [brand], [QtyRcd], [created_date], [updated_date], [season_id], [sell_style], [overall_status], [SLTD], [quantity_cmt], [user], [updated_time], [req_exfactory], [previous_pd_status], [previous_qa_status], [previous_design_status], [previous_brand_status], [previous_overall_status], [droa_needed])
     VALUES
           ('1', 'apple_100_dynamic_S24_L_1', 'apple_100_dynamic_S24', 'eapple', 'dynamic', '100', '24', 'Favourite_fruit', 'This_is_my_favourite', '{}', '6', 'L', 'Set_up_Ready', 'Approved', 'Approved', 'Rejected', '{}', NULL, '', '', '', '', '', 'DICKI', '2', '{}', '{}', 'S24', 'eappleL', '0', NULL, NULL, NULL, '15:54:01', '{}', NULL, NULL, NULL, NULL, NULL, '0')
"""

SAVE_DATA_FINAL_TP_VERIFIED = """
 INSERT into dbo.srt (reqno,sample_pid,style_pid,style,factory,color_code,season,project_name,description,request_date,Qty,
size,brand_status,design_status,pd_status,qa_status,request_recieved,promised_exfactory,pvf_cmt,brand_cmt,design_cmt,
pd_cmt,qa_cmt,brand,QtyRcd,created_date,updated_date,season_id,sell_style,overall_status,SLTD,quantity_cmt,[user],
updated_time,req_exfactory,previous_pd_status,previous_qa_status,previous_design_status,previous_brand_status,
previous_overall_status,droa_needed) VALUES (1,'eaaple_100_dynamic_S24_L_1','eaaple_100_dynamic_S24','eapple','dynamic','100',
'S24','this is my fav fruit','Favourite fruit','','','L','Set_up_Ready','Approved','Override','Approved','','','','','','','',
 'DICKI',7,'','','24','eappleL','','','','','','','','','','','',0);

INSERT into dbo.srt (reqno,sample_pid,style_pid,style,factory,color_code,season,project_name,description,request_date,Qty,
size,brand_status,design_status,pd_status,qa_status,request_recieved,promised_exfactory,pvf_cmt,brand_cmt,design_cmt,
pd_cmt,qa_cmt,brand,QtyRcd,created_date,updated_date,season_id,sell_style,overall_status,SLTD,quantity_cmt,[user],
updated_time,req_exfactory,previous_pd_status,previous_qa_status,previous_design_status,previous_brand_status,
previous_overall_status,droa_needed) VALUES (1,'eaaple_001_dynamic_S24_L_1','eaaple_001_dynamic_S24','eapple','dynamic','001',
'S24','this is my fav fruit','Favourite fruit','','','L','Set_up_Ready','Approved','Override','Approved','','','','','','','',
 'DICKI',7,'','','24','eappleL','','','','','','','','','','','',0);

  INSERT into dbo.status ([style],[tech_pack_status],[total_colors],[approved_colors],[pending_colors],[total_sizes],[approved_sizes]
      ,[pending_sizes],[Design_documents_status],[PD_documents_status],[QA_documents_status],[total_line_items],[season],[season_id]
      ,[sell_style],[vendor])VALUES ('eapple','0',0,0,0,0,0,0,'1','1','1',0,'S24','24','eappleL','')


      INSERT into dbo.stylelist ([style]
      ,[brand]
      ,[project_name]
      ,[collection]
      ,[wo]
      ,[status]
      ,[season_id]
      ,[season]
      ,[sell_style]
      ,[description]
      ,[factory]
      ,[color_code]
      ,[size]
      ,[droa_needed]) VALUES ('eapple','DICKI','This is my fav fruit','FASHION','LIFESTYLE','Product Ready','24','S23','eappleL',
      'Dickies Icon Woven Label Crew','dynamic','','','')

"""

SAVE_DATA_PRODUCT_READY = """
 INSERT into dbo.srt (reqno,sample_pid,style_pid,style,factory,color_code,season,project_name,description,request_date,Qty,
size,brand_status,design_status,pd_status,qa_status,request_recieved,promised_exfactory,pvf_cmt,brand_cmt,design_cmt,
pd_cmt,qa_cmt,brand,QtyRcd,created_date,updated_date,season_id,sell_style,overall_status,SLTD,quantity_cmt,[user],
updated_time,req_exfactory,previous_pd_status,previous_qa_status,previous_design_status,previous_brand_status,
previous_overall_status,droa_needed) VALUES (1,'eaaple_100_dynamic_S24_L_1','eaaple_100_dynamic_S24','eapple','dynamic','100',
'S24','this is my fav fruit','Favourite fruit','','','L',Null,'Approved','Override','Approved','','','','','','','',
 'DICKI',7,'','','24','eappleL','','','','','','','','','','','',0);

INSERT into dbo.srt (reqno,sample_pid,style_pid,style,factory,color_code,season,project_name,description,request_date,Qty,
size,brand_status,design_status,pd_status,qa_status,request_recieved,promised_exfactory,pvf_cmt,brand_cmt,design_cmt,
pd_cmt,qa_cmt,brand,QtyRcd,created_date,updated_date,season_id,sell_style,overall_status,SLTD,quantity_cmt,[user],
updated_time,req_exfactory,previous_pd_status,previous_qa_status,previous_design_status,previous_brand_status,
previous_overall_status,droa_needed) VALUES (1,'eaaple_001_dynamic_S24_L_1','eaaple_001_dynamic_S24','eapple','dynamic','001',
'S24','this is my fav fruit','Favourite fruit','','','L',Null,'Approved','Override','Approved','','','','','','','',
 'DICKI',7,'','','24','eappleL','','','','','','','','','','','',0);

  INSERT into dbo.stylelist ([style]
      ,[brand]
      ,[project_name]
      ,[collection]
      ,[wo]
      ,[status]
      ,[season_id]
      ,[season]
      ,[sell_style]
      ,[description]
      ,[factory]
      ,[color_code]
      ,[size]
      ,[droa_needed]) VALUES ('eapple','DICKI','This is my fav fruit','FASHION','LIFESTYLE','Product Ready','24','S23','eappleL',
      'Dickies Icon Woven Label Crew','dynamic','','','')

 """


SAVE_DATA_PRODUCT_READY_2 = """
 INSERT into dbo.srt (reqno,sample_pid,style_pid,style,factory,color_code,season,project_name,description,request_date,Qty,
size,brand_status,design_status,pd_status,qa_status,request_recieved,promised_exfactory,pvf_cmt,brand_cmt,design_cmt,
pd_cmt,qa_cmt,brand,QtyRcd,created_date,updated_date,season_id,sell_style,overall_status,SLTD,quantity_cmt,[user],
updated_time,req_exfactory,previous_pd_status,previous_qa_status,previous_design_status,previous_brand_status,
previous_overall_status,droa_needed) VALUES (1,'eaaple_100_dynamic_S24_L_1','eaaple_100_dynamic_S24','eapple','dynamic','100',
'S24','this is my fav fruit','Favourite fruit','','','L',Null,'Approved','Override','Approved','','','','','','','',
 'DICKI',7,'','','24','eappleL','','','','','','','','','','','',0);

INSERT into dbo.srt (reqno,sample_pid,style_pid,style,factory,color_code,season,project_name,description,request_date,Qty,
size,brand_status,design_status,pd_status,qa_status,request_recieved,promised_exfactory,pvf_cmt,brand_cmt,design_cmt,
pd_cmt,qa_cmt,brand,QtyRcd,created_date,updated_date,season_id,sell_style,overall_status,SLTD,quantity_cmt,[user],
updated_time,req_exfactory,previous_pd_status,previous_qa_status,previous_design_status,previous_brand_status,
previous_overall_status,droa_needed) VALUES (1,'eaaple_001_dynamic_S24_L_1','eaaple_001_dynamic_S24','eapple','dynamic','001',
'S24','this is my fav fruit','Favourite fruit','','','L',Null,'Approved','Override','Approved','','','','','','','',
 'DICKI',7,'','','24','eappleL','','','','','','','','','','','',0);

INSERT into dbo.stylelist ([style]
      ,[brand]
      ,[project_name]
      ,[collection]
      ,[wo]
      ,[status]
      ,[season_id]
      ,[season]
      ,[sell_style]
      ,[description]
      ,[factory]
      ,[color_code]
      ,[size]
      ,[droa_needed],[last_reminder]) VALUES ('eapple','DICKI','This is my fav fruit','FASHION','LIFESTYLE','In Development','24','S23','eappleL',
      'Dickies Icon Woven Label Crew','dynamic','','','','2023-06-06T12:34:56')

 """


DELETE_ALL_ERROR_NTFS = """
delete from dbo.email_ntfs
"""

DELETE_ALL_TABLE_RECORDS = """
delete from dbo.email_ntfs;
delete from dbo.master;
delete from dbo.status;
delete from dbo.stylelist;
delete from dbo.srf;
delete from dbo.srt;
delete from dbo.comments;
"""


data = [('DICKI', 'L', 'walt', '001'),
        ('DICKI', 'S', 'walt', '001'),
        ('DICKI', 'L', 'walt', '100')]

# '''
# given list of tuples, as index 0 as brand, index 1 as size, index 2 as factory, index 3 as color_code
# we need to group tuples based on brand,factory and color_code,
# and concatenate the size into one string, separated by ,
# return the output as a list of tuples, with brand,factory,color_code,size as index 0,1,2,3 respectively
# but with size as concatenated from similar tuples

# '''

# def group_by_brand_factory_color_code(data):
#     grouped_data = {}
#     for d in data:
#         key = (d[0], d[2], d[3])
#         if key in grouped_data:
#             grouped_data[key].append(d[1])
#         else:
#             grouped_data[key] = [d[1]]

#     output = []
#     for k, v in grouped_data.items():
#         output.append((k[0], k[1], k[2], ','.join(v)))

#     return output

# # print(group_by_brand_factory_color_code(data))


# '''
# from list of tuples, considering index 0 as brand_code , index 1 as size, index 2 as vendor and index 3 as color_code
# group the tuples based on brand_code, vendor and color_code, and concatenate the size into elements  separated by ,
# '''

# def group_by_color_code_brand_vendor(data):
#         grouped_data = {}
#         for d in data:
#             key = (d[2], d[3])
#             if key in grouped_data:
#                 grouped_data[key].append(d[1])
#             else:
#                 grouped_data[key] = [d[1]]

#         output = []
#         for k, v in grouped_data.items():
#             output.append((k[0], k[1], ','.join(v)))

#         return output
# # print(group_by_color_code_brand_vendor(data))




