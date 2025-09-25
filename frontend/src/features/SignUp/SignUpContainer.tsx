import { MdOutlineMailOutline } from "react-icons/md";
import { IoPersonOutline } from "react-icons/io5";
import { TbLockPassword } from "react-icons/tb";
import { IoEyeOffOutline, IoEyeOutline } from "react-icons/io5";
import microsoftLogo from "../../assets/microsoftLogo.png";
import googleLogo from "../../assets/googleLogo.png";

import { useState } from "react";

export default function SignUpContainer() {
    const [showPassword, setShowPassword] = useState(false);
    const handlePasswordToggle = () => setShowPassword((prev) => !prev);

    return <>
        <div className="
            bg-[#0A0A0A] 
            w-[410px] h-[580px] 
            border-[2px] border-[#282828] rounded-[15px] 
            flex flex-col items-center gap-5
            p-5">
                    
            <div>
                <p className="text-white geist-font text-[27px] font-[415] mt-3">Sign Up</p>
            </div>

            <div className="w-full pl-4 pr-4">
                <form className="flex flex-col gap-3">
                    <div className="relative">
                        <label htmlFor="fullName-input" className="text-[#8e8e8e] geist-font text-sm font-[375]">Full Name</label>
                        <input id="fullName-input" type="text" name="fullName" className="peer text-white text-sm pl-10 pr-2 h-9 w-full bg-neutral-950 border-[#282828] border-[2px] rounded-lg focus:border-[rgba(174,58,58,0.4)] focus:outline-none" />
                        <IoPersonOutline className="absolute left-[10px] top-[72%] -translate-y-1/2 text-[#8e8e8e] peer-focus:text-white text-sm pointer-events-none" />
                    </div>


                    <div className="relative">
                        <label htmlFor="email-input" className="text-[#8e8e8e] geist-font text-sm font-[375]">Email</label>
                        <input id="email-input" type="email" name="userEmail" className="peer text-white text-sm pl-10 pr-2 h-9 w-full bg-neutral-950 border-[#282828] border-[2px] rounded-lg focus:border-[rgba(174,58,58,0.4)] focus:outline-none" />
                        <MdOutlineMailOutline className="absolute left-[10px] top-[72%] transform -translate-y-1/2 text-[#8e8e8e] peer-focus:text-white text-sm pointer-events-none" />
                    </div>

                    <div className="relative">
                        <label htmlFor="password-input" className="text-[#8e8e8e] geist-font text-sm font-[375]">Password</label>
                        <input
                            id="password-input"
                            type={showPassword ? "text" : "password"}
                            name="userPassword"
                            className="peer text-white text-sm pl-10 pr-10 h-9 w-full bg-neutral-950 border-[#282828] border-[2px] rounded-lg focus:border-[rgba(174,58,58,0.4)] focus:outline-none"
                        />
                        <TbLockPassword className="absolute left-[10px] top-[70%] -translate-y-1/2 text-[#8e8e8e] peer-focus:text-white text-sm pointer-events-none" />
                            <button
                                type="button"
                                aria-label={showPassword ? "Hide password" : "Show password"}
                                onClick={handlePasswordToggle}
                                className="absolute right-[10px] top-[72%] -translate-y-1/2 text-[#8e8e8e] text-sm cursor-pointer hover:text-white transition-colors duration-300 bg-transparent border-none p-0 focus:outline-none focus-visible:ring-2 focus-visible:ring-[#ae3a3a] rounded">
                                {showPassword ? <IoEyeOutline /> : <IoEyeOffOutline />}
                            </button>
                    </div>

                    <div>
                        <button className="text-white bg-[#EF6262] w-full h-[35px] rounded-[6px] tracking-wider geist-font font-[250] text-[13px] mt-4 cursor-pointer transition-all duration-200 origin-center will-change-transform hover:scale-105 hover:bg-[#C04A4A] hover:shadow-[0_2px_12px_0_rgba(192,74,74,0.25)]">Create Account</button>
                    </div>

                </form>

                <div className="mt-8">
                    <div className="flex items-center w-full gap-1">
                        <div className="flex-1 h-[1px] bg-[#282828]" />
                        <span className="text-[#8E8E8E] geist-font font-[550] text-[11px] px-2">OR</span>
                        <div className="flex-1 h-[1px] bg-[#282828]" />
                    </div>
                </div>

                <div className="flex flex-row gap-4 mt-7">
                    <button className="flex items-center justify-center h-[34px] w-55 border-[2px] border-[#222222] rounded-lg shadow-sm bg-neutral-950 hover:bg-neutral-900 transition-all duration-200 cursor-pointer">
                        <img src={googleLogo} alt="Google logo" className="h-4 w-4" />
                    </button>
                    <button className="flex items-center justify-center h-[34px] w-55 border-[2px] border-[#222222] rounded-lg shadow-sm bg-neutral-950 hover:bg-neutral-900 transition-all duration-200 cursor-pointer">
                        <img src={microsoftLogo} alt="Microsoft logo" className="h-4 w-4" />
                    </button>
                </div>

                <div className="geist-font text-[12px] font-[150] tracking-wider mt-10 flex justify-center">
                    <p className="text-white">Already have an account? <a href="/login" className="text-[#EF6262] font-bold transition-all duration-500 hover:underline">Log in</a></p>
                </div>



            </div>




        </div>

    </>


}