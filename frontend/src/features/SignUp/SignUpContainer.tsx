import { MdOutlineMailOutline } from "react-icons/md";
import { IoPersonOutline } from "react-icons/io5";
import { TbLockPassword } from "react-icons/tb";




export default function SignUpContainer() {

    return <>
        <div className="
            bg-[#0A0A0A] 
            w-[405px] h-[550px] 
            border-[1.5px] border-[#282828] rounded-[15px] 
            flex flex-col items-center gap-10
            p-5">
                    
            <div>
                <p className="text-white geist-font text-[27px] font-[415]">Sign Up</p>
            </div>

            <div className="w-full pl-4 pr-4">
                <form className="flex flex-col gap-3">
                    <div className="relative">
                        <label htmlFor="fullName-input" className="text-[#8e8e8e] geist-font text-sm font-[450]">Full Name</label>
                        <input id="fullName-input" type="text" className="peer text-white text-sm pl-10 pr-2 h-9 w-full bg-neutral-950 border-[#282828] border-[1.5px] rounded-lg focus:border-[rgba(174,58,58,0.4)] focus:outline-none" />
                        <IoPersonOutline className="absolute left-[10px] top-[72%] -translate-y-1/2 text-[#8e8e8e] peer-focus:text-white text-sm pointer-events-none" />
                    </div>


                    <div className="relative">
                        <label htmlFor="email-input" className="text-[#8e8e8e] geist-font text-sm font-[450]">Email</label>
                        <input id="email-input" type="email" className="peer text-white text-sm pl-10 pr-2 h-9 w-full bg-neutral-950 border-[#282828] border-[1.5px] rounded-lg focus:border-[rgba(174,58,58,0.4)] focus:outline-none" />
                        <MdOutlineMailOutline className="absolute left-[10px] top-[72%] transform -translate-y-1/2 text-[#8e8e8e] peer-focus:text-white text-sm pointer-events-none" />
                    </div>

                    <div className="relative">
                        <label htmlFor="password-input" className="text-[#8e8e8e] geist-font text-sm font-[450]">Password</label>
                        <input id="password-input" type="password" className="peer text-white text-sm pl-10 pr-2 h-9 w-full bg-neutral-950 border-[#282828] border-[1.5px] rounded-lg focus:border-[rgba(174,58,58,0.4)] focus:outline-none" />
                        <TbLockPassword className="absolute left-[10px] top-[70%] -translate-y-1/2 text-[#8e8e8e] peer-focus:text-white text-sm pointer-events-none" />
                    </div>

                </form>


            </div>




        </div>

    </>


}