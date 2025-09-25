import sdsuLogo from '../assets/sdsuLogo.png';
export default function SiteHeader() {


    return <>

        <div className="flex justify-center">
            <button className="transform   origin-center will-change-transform transition-transform hover:scale-110 cursor-pointer">
            <div className="flex gap-4.5 mt-5">
            <img src={sdsuLogo} className="h-12 w-auto" alt="SDSU Logo" />
            <div className="w-[0.1px] h-10 mt-1.5 bg-gray-500"></div>
            <p className="text-white text-center text-sm mt-1 geist-font">Computer<br></br> Science</p>
            </div>
            </button>
        </div>
       
    </>

}