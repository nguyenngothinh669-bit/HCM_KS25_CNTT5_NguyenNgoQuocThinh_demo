def calculate_real_amount(amount,tax):
    return amount * (1 + tax/100) 

def classify_scale(real_amount):
    if real_amount < 2000000:
        return 'Nhỏ'
    elif real_amount < 10000000:
        return "Vừa"
    elif real_amount < 50000000:
        return 'Lớn'
    else:
        return 'Rất lớn'


def get_valid_id(transactions):
    while True:
        tx_id = input("Nhập mã giao dịch (Không để trống): ").strip()
        if not tx_id:
            print("Lỗi! Mã giao dịch bắt buộc phải nhập")
            continue
        exists = any(tx['id'] == tx_id.upper() for tx in transactions) 
        if exists:
            print("Lỗi: Mã giao dịch đã tồn tại trong hệ thống.")
            continue 
        return tx_id 


def get_valid_content():
    while True: 
        content = input("Nhập nội dung/lý do: ").strip()
        if not content:
            print("Lỗi: Nội dung thu chi bắt buộc phải nhập.")
            continue 
        return content 
    
def get_valid_type():
    while True:
        tx_type = input("Nhập loại giao dịch (Thu/Chi): ").strip().capitalize()
        if tx_type not in ["Thu","Chi"]:
            print("Lỗi: Loại giao dịch chỉ chấp nhận 'Thu' hoặc 'Chi'.") 
            continue 
        return tx_type 
    
def get_valid_amount():
    while True:
        try: 
            amount = float(input("Nhập số tiền phát sinh (>0): ").strip())
            if amount <=0 :
                print("Lỗi: Số tiền nhập vào phải lớn hơn 0")
                continue
            return amount 
        except ValueError:
            print("Lỗi: Dữ liệu nhập vào không hợp lệ. Vui lòng nhập lại số")
            
def get_valid_tax():
    while True:
        try: 
            tax = float(input("Nhập thuế suất (%) (>=0): ").strip())
            if tax < 0:
                print("Lỗi: Thuế suất nhập vào không được âm.")
                continue 
            return tax 
        except ValueError:
            print("Lỗi: Dữ liệu nhập vào không hợp lệ. Vui lòng nhập lại số.") 
            
def display_transactions(transactions):
    if not transactions: 
        print("Danh sách hiện tại đang trống!")
        return 
    
    header = f"| {'Mã TX':<10} | {'Nội dung':<35} | {'Loại':<5} | {'Tiền gốc':<15} | {'Thuế suất':<8} | {'Tiền thực tế':<15} | {'Quy mô':<10} |"
    print("-"*len(header))
    print(header) 
    print("-"*len(header)) 
    
    for tx in transactions:
        row = f"| {tx['id']:<10} | {tx['content']:<35} | {tx['type']:<5} | {tx['amount']:<15,.0f} | {tx['tax']:<8,.0f}  | {tx['real_amount']:<15,.0f} | {tx['scale']:<10} |"
        print(row) 
    print("-"*len(header))  
    
    
def add_transactions(transactions):
    print("\n--- GHI NHẬN GIAO DỊCH MỚI ---") 
    tx_id = get_valid_id(transactions)
    content = get_valid_content()
    tx_type = get_valid_type() 
    amount = get_valid_amount()
    tax = get_valid_tax() 
    
    real_amount = calculate_real_amount(amount,tax) 
    scale = classify_scale(real_amount) 
    
    new_transactions = {
        'id': tx_id.upper(),
        'content': content,
        'type': tx_type,
        'amount': amount,
        'tax':tax,
        'real_amount':real_amount,
        'scale':scale 
    }
    transactions.append(new_transactions) 
    print("Hoàn tất ghi nhận giao dịch mới thành công.") 
    
    
def find_transaction_index (transactions,tx_id):
    for i , tx in enumerate(transactions):
        if tx['id'] == tx_id.upper(): 
            return i 
    return -1 


def update_transactions(transactions):
    print("\n--- CẬP NHẬT CHỨNG TỪ GIAO DỊCH ---")
    if not transactions:
        print("Không có giao dịch nào trong danh sách để cập nhật!")
        return 
    tx_id = input("Nhập mã giao dịch cần cập nhật: ").strip().upper()
    
    index = find_transaction_index(transactions,tx_id)    
        
    if index == -1:
        print(f"Lỗi: Không tìm thấy mã giao dịch {tx_id} này trong hệ thống.")   
        return 
    
    print(f"Đã tìm thấy mã {tx_id}. Vui lòng cập nhật thông tin cần muốn:")
    content = get_valid_content()
    tx_type = get_valid_type()
    amount = get_valid_amount()
    tax = get_valid_tax() 
    
    real_amount = calculate_real_amount(amount,tax)
    scale = classify_scale(real_amount)
    
    transactions[index] = {
        'id': tx_id,
        'content': content,
        'type': tx_type,
        'amount': amount,
        'tax':tax,
        'real_amount':real_amount,
        'scale':scale 
    }
    print(f"Hoàn tất: Đã cập nhật thành công với mã {tx_id} này.")

def delete_transactions(transactions):
    print("\n--- XÓA GIAO DỊCH ---")
    tx_id = input("Nhập mã giao dich cần muốn xóa: ").strip().upper()
    if not transactions:
        print("Không có giao dịch nào trong danh sách để xóa!")
        return 
    index = find_transaction_index(transactions,tx_id)
    if index == -1:
        print(f"Lỗi: Không tìm thấy mã giao dịch {tx_id} này trong hệ thống.")   
        return  
    
    confirm = input("Bạn có chắc muốn xóa mã giao dịch này không? (Y/N): ").strip().upper()
    if confirm == "Y":
        transactions.pop(index)
        print("Hoàn tất: Đã xóa mã giao dịch này thành công ra khỏi hệ thống.")
    else:
        print("Đã hủy thao tác xóa") 

def search_transactions(transactions):
    print("\n--- TÌM KIẾM GIAO TIẾP ---")
    keyword = input("Nhập mã giao dich hoặc một phần nội dung cần tìm:").strip().upper()
    results = [] 
    if not transactions:
        print("Không có giao dịch nào trong danh sách để tìm kiếm!")
        return 
    if not keyword: 
        print("Từ khóa không được để trống!!")
        return 
    
    for tx in transactions:
        if keyword == tx['id'].upper() or keyword in tx['content'].upper(): 
            results.append(tx) 
            
    if not results:
        print("Không tìm thấy giao dịch nào phù hợp với từ khóa.")
    else:
        print(f"Tìm thấy {len(results)} kết quả:")
        display_transactions(results)

def statistics_transactions(transactions):
    print("\n--- THỐNG KÊ TỔNG DÒNG TIỀN ---")
    if not transactions:
        print("Danh sách hiện tại đang trống không thể thống kê!")
        return 
    
    stats = {"Rất lớn": 0,"Lớn": 0,"Vừa": 0,"Nhỏ": 0} 
    
    for tx in transactions:
        stats[tx['scale']] += 1 
        
    for scale ,count in stats.items():
        print(f"Quy mô {scale:<15}: {count} giao dịch")
        


def main():
    transactions = [{
            "id": "TX001",
            "content": "Doanh thu ban mo hinh Gundam",
            "type": "Thu",
            "amount": 15000000.0,
            "tax": 10.0,
            "real_amount": 16500000.0,
            "scale": "Lớn"
        },
        {
            "id": "TX002",
            "content": "Nhap switch Kailh linear",
            "type": "Chi",
            "amount": 3000000.0,
            "tax": 5.0,
            "real_amount": 31500000.0,
            "scale": "Vừa"
        },
        {
            "id": "TX003",
            "content": "Mua thiet bi Starlink mini",
            "type": "Chi",
            "amount": 8000000.0,
            "tax": 10.0,
            "real_amount": 8800000.0,
            "scale": "Vừa"
        }]
    while True:
        print("="*50)
        print("--- HỆ THỐNG QUẢN LÝ TÀI CHÍNH DÒNG TIỀN CLI ---")
        print("1. Hiển thị nhật ký giao dịch")
        print("2. Ghi nhận giao dịch mới") 
        print("3. Cập nhật chứng từ giao dịch")
        print("4. Xóa giao dịch")
        print("5. Tìm kiếm giao dịch")
        print("6. Thống kê tổng dòng tiền")
        print("7. Thoát chương trình") 
        print("="*50)
        choice = input("Nhập lựa chọn của bạn từ (1-8): ").strip()
        
        if not choice : 
            print("Lỗi: Vui lòng nhập chức năng 1-8. Không được để trống!")
            continue 
        
        
        match choice:
            case "1":
                display_transactions(transactions)
            case "2":
                add_transactions(transactions) 
            case "3":
                update_transactions(transactions)
            case "4":
                delete_transactions(transactions)
            case "5":
                search_transactions(transactions) 
            case "6":
                statistics_transactions(transactions)
            case "7":
                print("Thoát chương trình")
                break 
            case _:
                print("Lựa chọn bạn không hợp lệ . Vui lòng phải nhập lựa chọn từ 1 đến 8") 
                
                
if __name__ == "__main__":
    main() 