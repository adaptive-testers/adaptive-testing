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

            <div className="">
                <form>
                    <div>
                    <label htmlFor="firstName-input" className="text-white">First Name</label>
                    <input id="firstName-input" type="text" className="bg-white" />
                    </div>

                    <div>
                    <label htmlFor="lastName-input" className="text-white">Last Name</label>
                    <input id="lastName-input" type="text" className="bg-white" />
                    </div>

                    <div>
                    <label htmlFor="email-input" className="text-white">Email</label>
                    <input id="email-input" type="email" className="bg-white" />
                    </div>

                    <div>
                    <label htmlFor="password-input" className="text-white">Password</label>
                    <input id="password-input" type="password" className="bg-white" />
                    </div>

                </form>


            </div>




        </div>

    </>


}