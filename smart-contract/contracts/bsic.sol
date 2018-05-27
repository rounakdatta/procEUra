pragma solidity ^0.4.4;


contract OraclizeI {
    address public cbAddress;
    function query(uint _timestamp, string _datasource, string _arg) payable returns (bytes32 _id);
    function query_withGasLimit(uint _timestamp, string _datasource, string _arg, uint _gaslimit) payable returns (bytes32 _id);
    function query2(uint _timestamp, string _datasource, string _arg1, string _arg2) payable returns (bytes32 _id);
    function query2_withGasLimit(uint _timestamp, string _datasource, string _arg1, string _arg2, uint _gaslimit) payable returns (bytes32 _id);
    function getPrice(string _datasource) returns (uint _dsprice);
    function getPrice(string _datasource, uint gaslimit) returns (uint _dsprice);
    function useCoupon(string _coupon);
    function setProofType(byte _proofType);
    function setConfig(bytes32 _config);
    function setCustomGasPrice(uint _gasPrice);
}
contract OraclizeAddrResolverI {
    function getAddress() returns (address _addr);
}
contract usingOraclize {
    uint constant day = 60*60*24;
    uint constant week = 60*60*24*7;
    uint constant month = 60*60*24*30;
    byte constant proofType_NONE = 0x00;
    byte constant proofType_TLSNotary = 0x10;
    byte constant proofStorage_IPFS = 0x01;
    uint8 constant networkID_auto = 0;
    uint8 constant networkID_mainnet = 1;
    uint8 constant networkID_testnet = 2;
    uint8 constant networkID_morden = 2;
    uint8 constant networkID_consensys = 161;

    OraclizeAddrResolverI OAR;

    OraclizeI oraclize;
    modifier oraclizeAPI {
        if(address(OAR)==0) oraclize_setNetwork(networkID_auto);
        oraclize = OraclizeI(OAR.getAddress());
        _;
    }
    modifier coupon(string code){
        oraclize = OraclizeI(OAR.getAddress());
        oraclize.useCoupon(code);
        _;
    }

    function oraclize_setNetwork(uint8 networkID) internal returns(bool){
        if (getCodeSize(0x1d3b2638a7cc9f2cb3d298a3da7a90b67e5506ed)>0){ //mainnet
            OAR = OraclizeAddrResolverI(0x1d3b2638a7cc9f2cb3d298a3da7a90b67e5506ed);
            return true;
        }
        if (getCodeSize(0xc03a2615d5efaf5f49f60b7bb6583eaec212fdf1)>0){ //ropsten testnet
            OAR = OraclizeAddrResolverI(0xc03a2615d5efaf5f49f60b7bb6583eaec212fdf1);
            return true;
        }
        if (getCodeSize(0x20e12a1f859b3feae5fb2a0a32c18f5a65555bbf)>0){ //ether.camp ide
            OAR = OraclizeAddrResolverI(0x20e12a1f859b3feae5fb2a0a32c18f5a65555bbf);
            return true;
        }
        if (getCodeSize(0x93bbbe5ce77034e3095f0479919962a903f898ad)>0){ //norsborg testnet
            OAR = OraclizeAddrResolverI(0x93bbbe5ce77034e3095f0479919962a903f898ad);
            return true;
        }
        if (getCodeSize(0x51efaf4c8b3c9afbd5ab9f4bbc82784ab6ef8faa)>0){ //browser-solidity
            OAR = OraclizeAddrResolverI(0x51efaf4c8b3c9afbd5ab9f4bbc82784ab6ef8faa);
            return true;
        }
        return false;
    }

    function __callback(bytes32 myid, string result) {
        __callback(myid, result, new bytes(0));
    }
    function __callback(bytes32 myid, string result, bytes proof) {
    }

    function oraclize_getPrice(string datasource) oraclizeAPI internal returns (uint){
        return oraclize.getPrice(datasource);
    }
    function oraclize_getPrice(string datasource, uint gaslimit) oraclizeAPI internal returns (uint){
        return oraclize.getPrice(datasource, gaslimit);
    }

    function oraclize_query(string datasource, string arg) oraclizeAPI internal returns (bytes32 id){
        uint price = oraclize.getPrice(datasource);
        if (price > 1 ether + tx.gasprice*200000) return 0; // unexpectedly high price
        return oraclize.query.value(price)(0, datasource, arg);
    }
    function oraclize_query(uint timestamp, string datasource, string arg) oraclizeAPI internal returns (bytes32 id){
        uint price = oraclize.getPrice(datasource);
        if (price > 1 ether + tx.gasprice*200000) return 0; // unexpectedly high price
        return oraclize.query.value(price)(timestamp, datasource, arg);
    }
    function oraclize_query(uint timestamp, string datasource, string arg, uint gaslimit) oraclizeAPI internal returns (bytes32 id){
        uint price = oraclize.getPrice(datasource, gaslimit);
        if (price > 1 ether + tx.gasprice*gaslimit) return 0; // unexpectedly high price
        return oraclize.query_withGasLimit.value(price)(timestamp, datasource, arg, gaslimit);
    }
    function oraclize_query(string datasource, string arg, uint gaslimit) oraclizeAPI internal returns (bytes32 id){
        uint price = oraclize.getPrice(datasource, gaslimit);
        if (price > 1 ether + tx.gasprice*gaslimit) return 0; // unexpectedly high price
        return oraclize.query_withGasLimit.value(price)(0, datasource, arg, gaslimit);
    }
    function oraclize_query(string datasource, string arg1, string arg2) oraclizeAPI internal returns (bytes32 id){
        uint price = oraclize.getPrice(datasource);
        if (price > 1 ether + tx.gasprice*200000) return 0; // unexpectedly high price
        return oraclize.query2.value(price)(0, datasource, arg1, arg2);
    }
    function oraclize_query(uint timestamp, string datasource, string arg1, string arg2) oraclizeAPI internal returns (bytes32 id){
        uint price = oraclize.getPrice(datasource);
        if (price > 1 ether + tx.gasprice*200000) return 0; // unexpectedly high price
        return oraclize.query2.value(price)(timestamp, datasource, arg1, arg2);
    }
    function oraclize_query(uint timestamp, string datasource, string arg1, string arg2, uint gaslimit) oraclizeAPI internal returns (bytes32 id){
        uint price = oraclize.getPrice(datasource, gaslimit);
        if (price > 1 ether + tx.gasprice*gaslimit) return 0; // unexpectedly high price
        return oraclize.query2_withGasLimit.value(price)(timestamp, datasource, arg1, arg2, gaslimit);
    }
    function oraclize_query(string datasource, string arg1, string arg2, uint gaslimit) oraclizeAPI internal returns (bytes32 id){
        uint price = oraclize.getPrice(datasource, gaslimit);
        if (price > 1 ether + tx.gasprice*gaslimit) return 0; // unexpectedly high price
        return oraclize.query2_withGasLimit.value(price)(0, datasource, arg1, arg2, gaslimit);
    }
    function oraclize_cbAddress() oraclizeAPI internal returns (address){
        return oraclize.cbAddress();
    }
    function oraclize_setProof(byte proofP) oraclizeAPI internal {
        return oraclize.setProofType(proofP);
    }
    function oraclize_setCustomGasPrice(uint gasPrice) oraclizeAPI internal {
        return oraclize.setCustomGasPrice(gasPrice);
    }
    function oraclize_setConfig(bytes32 config) oraclizeAPI internal {
        return oraclize.setConfig(config);
    }

    function getCodeSize(address _addr) constant internal returns(uint _size) {
        assembly {
            _size := extcodesize(_addr)
        }
    }


    function parseAddr(string _a) internal returns (address){
        bytes memory tmp = bytes(_a);
        uint160 iaddr = 0;
        uint160 b1;
        uint160 b2;
        for (uint i=2; i<2+2*20; i+=2){
            iaddr *= 256;
            b1 = uint160(tmp[i]);
            b2 = uint160(tmp[i+1]);
            if ((b1 >= 97)&&(b1 <= 102)) b1 -= 87;
            else if ((b1 >= 48)&&(b1 <= 57)) b1 -= 48;
            if ((b2 >= 97)&&(b2 <= 102)) b2 -= 87;
            else if ((b2 >= 48)&&(b2 <= 57)) b2 -= 48;
            iaddr += (b1*16+b2);
        }
        return address(iaddr);
    }


    function strCompare(string _a, string _b) internal returns (int) {
        bytes memory a = bytes(_a);
        bytes memory b = bytes(_b);
        uint minLength = a.length;
        if (b.length < minLength) minLength = b.length;
        for (uint i = 0; i < minLength; i ++)
            if (a[i] < b[i])
                return -1;
            else if (a[i] > b[i])
                return 1;
        if (a.length < b.length)
            return -1;
        else if (a.length > b.length)
            return 1;
        else
            return 0;
   }

    function indexOf(string _haystack, string _needle) internal returns (int)
    {
        bytes memory h = bytes(_haystack);
        bytes memory n = bytes(_needle);
        if(h.length < 1 || n.length < 1 || (n.length > h.length))
            return -1;
        else if(h.length > (2**128 -1))
            return -1;
        else
        {
            uint subindex = 0;
            for (uint i = 0; i < h.length; i ++)
            {
                if (h[i] == n[0])
                {
                    subindex = 1;
                    while(subindex < n.length && (i + subindex) < h.length && h[i + subindex] == n[subindex])
                    {
                        subindex++;
                    }
                    if(subindex == n.length)
                        return int(i);
                }
            }
            return -1;
        }
    }

    function strConcat(string _a, string _b, string _c, string _d, string _e) internal returns (string){
        bytes memory _ba = bytes(_a);
        bytes memory _bb = bytes(_b);
        bytes memory _bc = bytes(_c);
        bytes memory _bd = bytes(_d);
        bytes memory _be = bytes(_e);
        string memory abcde = new string(_ba.length + _bb.length + _bc.length + _bd.length + _be.length);
        bytes memory babcde = bytes(abcde);
        uint k = 0;
        for (uint i = 0; i < _ba.length; i++) babcde[k++] = _ba[i];
        for (i = 0; i < _bb.length; i++) babcde[k++] = _bb[i];
        for (i = 0; i < _bc.length; i++) babcde[k++] = _bc[i];
        for (i = 0; i < _bd.length; i++) babcde[k++] = _bd[i];
        for (i = 0; i < _be.length; i++) babcde[k++] = _be[i];
        return string(babcde);
    }

    function strConcat(string _a, string _b, string _c, string _d) internal returns (string) {
        return strConcat(_a, _b, _c, _d, "");
    }

    function strConcat(string _a, string _b, string _c) internal returns (string) {
        return strConcat(_a, _b, _c, "", "");
    }

    function strConcat(string _a, string _b) internal returns (string) {
        return strConcat(_a, _b, "", "", "");
    }

    // parseInt
    function parseInt(string _a) internal returns (uint) {
        return parseInt(_a, 0);
    }

    // parseInt(parseFloat*10^_b)
    function parseInt(string _a, uint _b) internal returns (uint) {
        bytes memory bresult = bytes(_a);
        uint mint = 0;
        bool decimals = false;
        for (uint i=0; i<bresult.length; i++){
            if ((bresult[i] >= 48)&&(bresult[i] <= 57)){
                if (decimals){
                   if (_b == 0) break;
                    else _b--;
                }
                mint *= 10;
                mint += uint(bresult[i]) - 48;
            } else if (bresult[i] == 46) decimals = true;
        }
        if (_b > 0) mint *= 10**_b;
        return mint;
    }

    function uint2str(uint i) internal returns (string){
        if (i == 0) return "0";
        uint j = i;
        uint len;
        while (j != 0){
            len++;
            j /= 10;
        }
        bytes memory bstr = new bytes(len);
        uint k = len - 1;
        while (i != 0){
            bstr[k--] = byte(48 + i % 10);
            i /= 10;
        }
        return string(bstr);
    }



}

contract bsic is usingOraclize {


   function  bsic() {
     getRandom();
   }
    struct tender {
        string organisation;
        string tender_ref_no;
        uint tender_id;
        bool open_tender;
        string tender_category;
        string tech_doc;
        string finance_doc;
        string bid_opening_date;
        string bid_close_date;
        uint value_of_tender;
    }

    struct bidder {
      string companyName;
      address add;
      uint regno;
      string regAdd;
      string bidderType;
      string city;
      string state;
      uint postalCode;
      string Pan;
      string natureOfBusiness;
      string legalStatus;
      string companyCategory;
      uint repu;
      uint repu_counter;
    }


    struct tenderFee {
      uint feeAmount;
      string payTo;
      string payAt;
      bool feeExemptAllow;
    }

    struct criticalDates {
      string publishDate;
      string bidSubmissionStartDate;
      string bidOpeningDate;
    }


    struct bids {
        uint bid_no;
        uint tender_id;
        uint bidder_reg_no;
        uint bid;
    }

    mapping (uint => tender) tender_id_to_tender_mapping;
    mapping (uint => bidder) bidder_id_to_bidder_mapping;
    mapping (uint => tenderFee) tender_id_to_tender_fee_mapping;
    mapping (uint => bids) tenderIdToBids;
    mapping (uint => uint) tender_id_to_counter;
    mapping (uint => tender) bid_to_tender_mapping;
    mapping (address => uint) bidder_address_mapping;

    function bidderEnrollment(string cname,uint reg,string regadd,string biddertype,string city,string state,uint post,string pan,string nature,string legals,string ccat) {
      bidder_id_to_bidder_mapping[reg]=bidder(cname,msg.sender,reg,regadd,biddertype,city,state,post,pan,nature,legals,ccat,0,0);
      bidder_address_mapping[msg.sender]=reg;
    }
  uint[] tenderarr;
    function addTender(string org, string tenderRefNo, uint tenderID, bool tenderOpenStatus, string tenderCategory, string techDoc, string financeDoc, string bidOpen, string bidClose, uint tenderVal) {
      tender_id_to_tender_mapping[tenderID].organisation = org;
      tender_id_to_tender_mapping[tenderID].tender_ref_no = tenderRefNo;
      tender_id_to_tender_mapping[tenderID].tender_id = tenderID;
      tender_id_to_tender_mapping[tenderID].open_tender = tenderOpenStatus;
      tender_id_to_tender_mapping[tenderID].tender_category = tenderCategory;
      tender_id_to_tender_mapping[tenderID].tech_doc = techDoc;
      tender_id_to_tender_mapping[tenderID].finance_doc = financeDoc;
      tender_id_to_tender_mapping[tenderID].bid_opening_date = bidOpen;
      tender_id_to_tender_mapping[tenderID].bid_close_date = bidClose;
      tender_id_to_tender_mapping[tenderID].value_of_tender = tenderVal;
      tender_id_to_counter[tenderID] = 0;
      tenderarr.push(tenderID);
      tendertobidderarray[tenderID]=[0];
    }

    function gettenderarr() constant returns(uint[])
    {
       return tenderarr;
    }

    function showtenderdetails(uint tenderID) constant returns(string,string,uint,bool,string,string)
    {
        return(tender_id_to_tender_mapping[tenderID].organisation,tender_id_to_tender_mapping[tenderID].tender_ref_no,tender_id_to_tender_mapping[tenderID].tender_id,tender_id_to_tender_mapping[tenderID].open_tender,tender_id_to_tender_mapping[tenderID].tender_category,tender_id_to_tender_mapping[tenderID].tech_doc);
    }

    function showtenderdetails2(uint tenderID) constant returns(string,string,string,uint)
    {
        return(tender_id_to_tender_mapping[tenderID].finance_doc,tender_id_to_tender_mapping[tenderID].bid_opening_date,tender_id_to_tender_mapping[tenderID].bid_close_date,tender_id_to_tender_mapping[tenderID].value_of_tender);
    }

mapping (uint => uint[]) tendertobidderarray;
    function bid_to_tender(uint tender_uid, uint bid_det) {
      uint bidder_reg_no=bidder_address_mapping[msg.sender];
         tenderIdToBids[tender_uid] = bids(tender_id_to_counter[tender_uid], tender_uid, bidder_reg_no, bid_det);
         tendertobidderarray[tender_uid].push(bidder_reg_no);
         tender_id_to_counter[tender_uid]++;
         bid_to_tender_mapping[bidder_reg_no]=tender_id_to_tender_mapping[tender_uid];
         biddercount[bidder_reg_no]=0;
    }

    function displaybidders(uint tenderid) constant returns(uint[]) {
      return tendertobidderarray[tenderid];
    }

    function give_vote(uint rep_int, uint bidder_id) {
        uint a = bidder_id_to_bidder_mapping[bidder_id].repu;
        uint b = bidder_id_to_bidder_mapping[bidder_id].repu_counter;
        a = (a+rep_int);
        bidder_id_to_bidder_mapping[bidder_id].repu = a;
        bidder_id_to_bidder_mapping[bidder_id].repu_counter++;
    }

    function  show_bidder_rating(uint bidderid) constant returns(uint rating) {
        rating=(bidder_id_to_bidder_mapping[bidderid].repu)/(bidder_id_to_bidder_mapping[bidderid].repu_counter);
    }


    struct selector {
      uint regno;
      address add;
    }

   uint[] public selectorarr;
    mapping ( uint => selector) selectorregtoselector;
    function add_selector(uint regno) {
      selectorregtoselector[regno]=selector(regno,msg.sender);
      selectorarr.push(regno);
    }

    uint public result;
    bytes32 public oraclizeID;


    function getRandom() payable {
      oraclizeID = oraclize_query("WolframAlpha","random number between 1 and 1000");
    }

    function __callback(bytes32 _oraclizeID,string _result) {
      if(msg.sender!=oraclize_cbAddress())
        throw;
      result=parseInt(_result);
    }

    uint[] public selectedselectors;


    function disselselectors(uint tender_id) constant returns(uint[])
    {
        return tendertoselector[tender_id];
    }


    mapping (uint  => uint[]) tendertoselector;

    function selectrandomselector(uint tender_id) {
        
        uint selarrlength=selectorarr.length;
        
        tendertoselector[tender_id]=[0];
        for(uint i=0;i<5;i++)
        {
            uint loc=result%selarrlength;
            selectedselectors.push(selectorarr[loc]);
            tendertoselector[tender_id].push(selectorarr[loc]);
            result+=109;
        }
        result+=now;
    }


   mapping (uint => uint) biddercount;

    function  opinion(uint tenderid,uint bidder_reg_no) {

         biddercount[bidder_reg_no]++;

    }


   mapping (uint => uint) tendertowinner;
    function checkwinner(uint tender_id) {
      uint[] arr=tendertobidderarray[tender_id];
      uint max=biddercount[arr[0]];
      uint winner;
           for(uint i=0;i<arr.length;i++)
           {
             if(biddercount[arr[i]]>max)
             {
               max=biddercount[arr[i]];
               winner=arr[i];
             }
           }
           tendertowinner[tender_id]=winner;
    }

    function displaywinner(uint tenderid) constant returns (uint) {
      return tendertowinner[tenderid];
    }







}
